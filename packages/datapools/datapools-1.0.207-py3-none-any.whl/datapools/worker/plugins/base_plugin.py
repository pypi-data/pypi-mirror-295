import base64
import traceback
import io
import sys
import subprocess
import json
from abc import ABCMeta, abstractmethod
from hashlib import md5
from cachetools import TTLCache, cached
from time import time
from typing import AsyncGenerator, Union, Optional, Callable, List, Dict, Any
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import magic
from dateutil import parser as date_parser

# from dateutil.tz import tzutc
from datetime import datetime

import dns.resolver
import httpx
from PIL import Image
from PIL.ExifTags import Base as ExifTagsList
import mutagen
import calendar

from playwright.async_api import async_playwright, Browser, Playwright as AsyncPlaywright, BrowserContext, Page, Locator

from ...common.logger import logger
from ...common.types import (
    BaseCrawlerResult,
    CrawlerBackTask,
    DatapoolContentType,
    WorkerTask,
    StudyUrlTask,
)
from ..types import BaseTag
from ..utils import canonicalize_url
from ..types import WorkerContext

MAGIC_MIN_BYTES = 512000  # audio/mpeg seems to require that much..


try:
    from bs4 import BeautifulSoup
except ImportError:
    pass

import re


class BasePluginException(Exception):
    pass


class UnexpectedContentTypeException(BasePluginException):
    pass


class DownloadFailureException(BasePluginException):
    pass


class CachedPairs:
    def __init__(self):
        self.data = {}

    def contains(self, key, ttl):
        return key in self.data and time() - self.data[key][1] < ttl

    def set(self, key, value):
        self.data[key] = (value, time())

    def get(self, key):
        return self.data[key][0]


class Cache:
    def __init__(self):
        self.value = None
        self.time = None

    def is_valid(self, ttl):
        return self.time is not None and time() - self.time < ttl

    def set(self, value):
        self.value = value
        self.time = time()

    def get(self):
        return self.value

    def __repr__(self):
        return f"Cache({self.value=}, {self.time=})"


class PlaywrightBrowserContextManager:
    context: BrowserContext
    url: str
    page: Page

    def __init__(self, context: BrowserContext, url: str, timeout):
        self.context = context
        self.url = url
        self.timeout = timeout

    async def __aenter__(self):
        self.page = await self.context.new_page()
        await self.page.goto(str(self.url), timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.page.close()


class PlaywrightBrowser:
    playwright: AsyncPlaywright
    browser: Browser
    context: BrowserContext

    async def start(self):
        logger.info("starting browser")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.context = await self.browser.new_context(viewport={"width": 1920, "height": 1024})
        logger.info("started browser")

    def open(self, url: str, timeout: int | float):
        return PlaywrightBrowserContextManager(self.context, url, timeout)


study_url_browser = PlaywrightBrowser()


class BasePlugin(metaclass=ABCMeta):

    license_filename = "LICENSE.txt"
    license_max_size = 1024
    _busy_count = 0
    _is_busy = False
    _regexps = {
        re.compile(r"(?:^|.*\s)(?:https://)*openlicense.ai/(n/|t/|\b)(\w+)(?:$|\s)", re.MULTILINE | re.DOTALL): True,
    }
    copyright_tags_cache: CachedPairs
    platform_tag_cache: Cache
    rp: Optional[RobotFileParser] = None

    def __init__(self, ctx: WorkerContext):
        self.ctx = ctx
        self._is_busy = False
        self.copyright_tags_cache = CachedPairs()
        self.platform_tag_cache = Cache()

    def __del__(self):
        if self._is_busy:
            self.is_busy = False  # calling @is_busy.setter
            logger.warning("was busy on destruction!!")

    @property
    def is_busy(self):
        return self._is_busy

    @is_busy.setter
    def is_busy(self, b: bool):
        if self._is_busy != b:
            self._is_busy = b
            if b:
                type(self)._busy_count += 1
                logger.info(f"busy count of plugin {type(self).__name__} is {type(self)._busy_count} (incremented)")
            else:
                type(self)._busy_count -= 1
                logger.info(f"busy count of plugin {type(self).__name__} is {type(self)._busy_count} (decremented)")

    @classmethod
    def get_busy_count(cls):
        return cls._busy_count

    async def download(self, url, headers={}, follow_redirects=True, max_redirects=5, timeout=5):
        logger.info(f"BasePlugin.download {url=}")
        try:
            async with httpx.AsyncClient(max_redirects=max_redirects, timeout=timeout) as client:
                r = await client.get(url, follow_redirects=follow_redirects, headers=headers, timeout=timeout)
                return r.content

        except Exception as e:
            logger.error(f"failed get content of {url}: {e}")

    async def async_read_url(
        self,
        url,
        expected_type: Optional[DatapoolContentType] = None,
        headers={},
        follow_redirects=True,
        max_redirects=5,
    ):
        logger.info(f"BasePlugin.async_read_url {url=}")

        # will try to check content type by http content-type header or ( if header check fails ) by content itself
        is_header_checked = False
        is_content_checked = False
        is_type_ok = False
        type_bytes = bytes()
        try:
            async with httpx.AsyncClient(max_redirects=max_redirects) as client:
                async with client.stream("GET", url, follow_redirects=follow_redirects, headers=headers) as stream:
                    # logger.info(f"{stream.url=}")
                    if stream.status_code != 200:
                        raise DownloadFailureException(stream.status_code)
                    async for chunk in stream.aiter_bytes():
                        # logger.info(f"{chunk=}")
                        if expected_type and not is_type_ok:
                            type_bytes += chunk

                            resp_type = None
                            if not is_header_checked:
                                # check by content-type header
                                ct = stream.headers.get("content-type")
                                if ct:
                                    is_header_checked = True
                                    try:
                                        resp_type = self.get_content_type_by_mime_type(ct)
                                        logger.info(f"async_read_url:{resp_type=} by header")
                                        if resp_type == expected_type:
                                            is_type_ok = True
                                    except UnexpectedContentTypeException:
                                        pass

                            # then try to check by content itself
                            if not is_content_checked and not is_type_ok:
                                if len(type_bytes) >= MAGIC_MIN_BYTES:
                                    is_content_checked = True
                                    try:
                                        resp_type = self.get_content_type_by_content(type_bytes)
                                        logger.info(f"async_read_url:{resp_type=} by content")
                                        if resp_type == expected_type:
                                            is_type_ok = True
                                    except UnexpectedContentTypeException:
                                        pass

                            # if both header and content check and both do not match then raise
                            if is_header_checked and is_content_checked and not is_type_ok:
                                raise UnexpectedContentTypeException(
                                    f"Unexpected content type: {expected_type} vs {resp_type}"
                                )
                        else:
                            if type_bytes:
                                yield type_bytes
                                type_bytes = bytes()

                            yield chunk
                    if type_bytes:
                        yield type_bytes
        except httpx.ReadTimeout as e:
            logger.error("async_read_url ReadTimeout exception")
            raise DownloadFailureException from e
        except Exception as e:
            logger.error(f"async_read_url Exception: {e}")
            logger.error(traceback.format_exc())
            raise DownloadFailureException from e

    @staticmethod
    def parse_url(url):
        return urlparse(url)

    @staticmethod
    @abstractmethod
    def is_supported(url) -> bool: ...

    def is_allowed_by_robots_txt(self, url: str) -> bool:
        if self.rp is None:
            self.rp = RobotFileParser()

        p = self.parse_url(url)
        robots_url = f"{p.scheme}//{p.netloc}/robots.txt"
        self.rp.set_url(robots_url)
        try:
            self.rp.read()
        except:
            return True
        return self.rp.can_fetch("*", url)

    @staticmethod
    def is_same_or_subdomain(dom1, dom2) -> bool:
        # blabla.domain.com could be considered a subdomain of www.domain.com
        if dom2[0:4] == "www.":
            dom2 = dom2[4:]
        if dom1 == dom2:
            return True
        s1 = dom1.split(".")
        s2 = dom2.split(".")
        return s1[-len(s2) : :] == s2

    @staticmethod
    def is_sub_url(url: str, sub_url: str) -> bool:
        p_url = BasePlugin.parse_url(url)
        p_sub = BasePlugin.parse_url(sub_url)
        if p_url.netloc != p_sub.netloc and p_sub.netloc != "":
            return False
        return p_sub.path.find(p_url.path) == 0

    @staticmethod
    def get_local_url(href, page_url, allow_external=False):
        # logger.info(f"get_local_url {href=} {page_url=}")
        pc = urlparse(page_url)
        # logger.info(pc)
        p = urlparse(href)
        # logger.info(f"{p=}")
        if (p.netloc == "" and p.path != "") or BasePlugin.is_same_or_subdomain(p.netloc, pc.netloc):
            return urljoin(page_url, href)
        elif allow_external and p.netloc != "":  # not local, but full url
            return href
        return False

    @staticmethod
    def merge_head_tail(head, tail):
        # returns intersection length
        m = len(head)
        n = len(tail)

        for i in range(max(0, m - n), m):
            head_slice = head[i:]
            tail_slice = tail[0 : m - i]
            # print(i, head_slice, tail_slice)

            if head_slice == tail_slice:
                return head + tail[i:]
        return head + tail

    @abstractmethod
    def process(self, task: WorkerTask) -> AsyncGenerator[BaseCrawlerResult, None]: ...

    async def study(self, task: StudyUrlTask, timeout: int = 3000) -> List[BaseTag]:
        async with study_url_browser.open(task.url, timeout=timeout) as cm:
            logger.info(f"studying {cm.page.url=}")

            real_url = cm.page.url
            if not self.get_local_url(real_url, task.url):
                logger.info("redirected to different domain")
                return []

            url = real_url

            tags = []

            p = BasePlugin.parse_url(url)
            platform_tag = await self.get_platform_tag(p.netloc, cm.page, 3600)
            if platform_tag:
                tags.append(platform_tag)

            return tags

    @staticmethod
    def is_imported(module):
        return module in sys.modules

    @classmethod
    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    def parse_dns_tag(cls, domain) -> Union[BaseTag, None]:
        logger.info(f"parse_dns_tag {domain=}")
        try:
            records = dns.resolver.resolve(domain, "TXT")
            logger.info(f"{records=}")
            for record in records:
                tag = BasePlugin.parse_tag_in_str(str(record))
                if tag is not None:
                    return tag
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.LifetimeTimeout:
            pass
        return None

    @classmethod
    async def parse_meta_tag(cls, content, meta_name) -> Optional[BaseTag]:
        if BasePlugin.is_imported("bs4") and type(content) is BeautifulSoup:
            return BasePlugin.parse_tag_in_bs_content(content, "meta")
        if BasePlugin.is_imported("playwright.async_api") and type(content) is Page:
            metas = content.locator(f'meta[name="{meta_name}"]')
            for meta in await metas.all():
                c = await meta.get_attribute("content")

                tag = BasePlugin.parse_tag_in_str(c)
                if tag is not None:
                    return tag
        return None

    @classmethod
    def parse_tag_in_str(cls, string) -> Union[BaseTag, None]:
        # logger.info(f"parse_tag_in_str {string=}")
        for regexp, keepout in BasePlugin._regexps.items():
            tag = regexp.match(string)
            if tag is not None:
                if keepout is False:
                    return BaseTag(tag.group(1))
                else:
                    return BaseTag(tag.group(2), tag.group(1) == "n/")
        return None

    @classmethod
    def parse_tag_in_bs_content(cls, content: BeautifulSoup, locator: str) -> Optional[BaseTag]:
        for regexp, deniable in BasePlugin._regexps.items():
            tag = content.find(locator, attrs={"content": regexp})
            if tag is not None:
                if deniable is False:
                    return BaseTag(tag.group(1))
                else:
                    return BaseTag(tag.group(2), tag.group(1) == "n/")
        return None

    @classmethod
    async def parse_tag_in(cls, content, loc: str = "") -> Optional[BaseTag]:
        if type(content) is str:
            return BasePlugin.parse_tag_in_str(content)
        elif BasePlugin.is_imported("bs4") and type(content) is BeautifulSoup:
            return BasePlugin.parse_tag_in_bs_content(content, loc)

        elif BasePlugin.is_imported("playwright.async_api") and isinstance(content, (Page, Locator)):
            elems = content.locator(loc)
            for elem in await elems.all():
                c = await elem.text_content()
                if c is not None:
                    return BasePlugin.parse_tag_in_str(c)
        return None

    @staticmethod
    def get_content_type_by_mime_type(mime) -> DatapoolContentType:
        # logger.info(f"{mime=}")
        parts = mime.split("/")
        if parts[0] == "image":
            return DatapoolContentType.Image
        if parts[0] == "video" or mime == "application/mxf":
            return DatapoolContentType.Video
        if parts[0] == "audio":
            return DatapoolContentType.Audio
        if parts[0] == "text" or mime == "application/json":
            return DatapoolContentType.Text

        raise UnexpectedContentTypeException(f"not supported {mime=}")

    @staticmethod
    def get_content_type_by_content(content: Union[bytes, str, io.IOBase]) -> DatapoolContentType:
        if isinstance(content, (bytes, str)):
            buffer = content
        elif isinstance(content, io.IOBase):
            content.seek(0, 0)
            buffer = content.read(MAGIC_MIN_BYTES)  # TODO: enough?
        else:
            raise BasePluginException(f"not supported input: {type(content)}")
        mime = magic.from_buffer(buffer, mime=True)
        if mime:
            return BasePlugin.get_content_type_by_mime_type(mime)
        raise BasePluginException("not supported content")

    @classmethod
    def _getexif(cls, content: Union[bytes, io.IOBase]) -> Image.Exif:
        if isinstance(content, bytes):
            image = Image.open(io.BytesIO(content))
        elif isinstance(content, io.IOBase):
            image = Image.open(content)  # type: ignore
        else:
            raise Exception(f"Unsupport image content {type(content)=}")
        return image.getexif()

    @classmethod
    def parse_image_tag(cls, content: Union[bytes, io.IOBase]) -> Optional[BaseTag]:
        # load image from bytes content, parse Copyright exif field for a license tag
        try:
            exifdata = cls._getexif(content)
            cp = exifdata.get(ExifTagsList.Copyright)
            # logger.info( f'{cp=} {type(cp)=}')

            if isinstance(cp, str):
                return cls.parse_tag_in_str(cp)
        except Exception as e:
            logger.error(f"Failed process image (tag): {e}")
        return None

    @classmethod
    def parse_image_datetime(cls, content: Union[bytes, io.IOBase]) -> Optional[int]:
        try:
            exifdata = cls._getexif(content)
            dt = exifdata.get(ExifTagsList.DateTimeOriginal) or exifdata.get(ExifTagsList.DateTime)
            if isinstance(dt, str):
                return cls.parse_datetime(dt, "%Y:%m:%d %H:%M:%S")
        except Exception as e:
            logger.error(f"Failed process image (datetime): {e}")
        return None

    @classmethod
    def get_audio_meta(cls, content: Union[bytes, io.IOBase]) -> Optional[dict]:
        if isinstance(content, bytes):
            return mutagen.File(io.BytesIO(content))
        if isinstance(content, io.IOBase):
            return mutagen.File(content)
        raise Exception(f"Unsupport audio content {type(content)=}")

    @classmethod
    def _get_video_meta(cls, content: Union[bytes, io.IOBase]) -> Optional[dict]:
        """returns video stream info of a video file using ffprobe command line interface"""
        args = ["ffprobe", "-v", "quiet", "-i", "pipe:0", "-show_streams", "-show_format", "-print_format", "json"]

        if isinstance(content, bytes):
            logger.info("video meta by bytes")
            p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # type: ignore
            out, err = p.communicate(input=content)
        elif isinstance(content, io.IOBase):
            logger.info("video meta by IOBase")
            content.seek(0, 0)
            p = subprocess.Popen(args, stdin=content.fileno(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # type: ignore
            out, err = p.communicate()
        if p.returncode != 0:
            logger.error(f"Failed call ffprobe: {out=} {err=} {p.returncode=}")
            return None
        resp = out.decode("utf-8")
        # logger.info(resp)
        return json.loads(resp)

    @classmethod
    def parse_audio_tag(cls, content: Union[bytes, io.IOBase]) -> Optional[BaseTag]:
        # https://mutagen-specs.readthedocs.io/en/latest/id3/id3v2.2.html
        # http://www.unixgods.org/Ruby/ID3/docs/ID3_comparison.html
        try:
            m = cls.get_audio_meta(content)
            if m:
                for key in ("TCOP", "WCOP", "TCR", "WCP"):
                    copyright = m.get(key)
                    if copyright:
                        for t in copyright.text:
                            tag = BasePlugin.parse_tag_in_str(t)
                            if tag:
                                return tag
        except Exception as e:
            logger.error(f"Failed process audio (datetime): {e}")
        return None

    @classmethod
    def parse_audio_datetime(cls, content: Union[bytes, io.IOBase]) -> Optional[int]:
        # https://mutagen-specs.readthedocs.io/en/latest/id3/id3v2.2.html
        # http://www.unixgods.org/Ruby/ID3/docs/ID3_comparison.html
        try:
            m = cls.get_audio_meta(content)
            if m:
                dt = m.get("TDRC")
                if dt:
                    return cls.parse_datetime(str(dt))

                y = m.get("TYE") or m.get("TYER")  # YYYY
                if y:
                    dt = str(y)
                    fmt = "%Y"

                    dm = m.get("TDA") or m.get("TDAT")  # DDMM
                    if dm:
                        dt += str(dm)
                        fmt += "%d%m"

                    t = m.get("TIM") or m.get("TIME")  # HHMM
                    if t:
                        dt += str(t)
                        fmt += "%H%M"

                    if dt:
                        return cls.parse_datetime(dt, fmt)

        except Exception as e:
            logger.error(f"Failed process audio (datetime): {e}")
            # logger.error(traceback.format_exc())
        return None

    @classmethod
    def parse_video_tag(cls, content: Union[bytes, io.IOBase]) -> Optional[BaseTag]:
        info = BasePlugin._get_video_meta(content)
        logger.info(info)
        if info and "format" in info and "copyright" in info["format"]["tags"]:
            return BasePlugin.parse_tag_in_str(info["format"]["tags"]["copyright"])
        return None

    @classmethod
    def parse_video_datetime(cls, content: Union[bytes, io.IOBase]) -> Optional[int]:
        info = BasePlugin._get_video_meta(content)
        logger.info(info)
        if info and "streams" in info:
            for stream in info["streams"]:
                if stream.get("codec_type") == "video":
                    if "tags" in stream and "creation_time" in stream["tags"]:
                        return BasePlugin.parse_datetime(stream["tags"]["creation_time"])
                    break
        return None

    @classmethod
    def parse_content_tag(cls, content: Union[bytes, io.IOBase], type: DatapoolContentType) -> Optional[BaseTag]:
        if type == DatapoolContentType.Image:
            return BasePlugin.parse_image_tag(content)
        elif type == DatapoolContentType.Audio:
            return BasePlugin.parse_audio_tag(content)
        if type == DatapoolContentType.Video:
            return BasePlugin.parse_video_tag(content)
        raise BasePluginException(f"parse_content_tag: not supported content type {type}")

    async def get_platform_tag(self, domain, content, ttl=3600, meta_name=None) -> Union[BaseTag, None]:
        # logger.info( f'get_platform_tag {self.platform_tag_cache=}')
        # logger.info(f'now={time()}' )
        # logger.info(f'diff={time() - self.platform_tag_cache.time if self.platform_tag_cache.time is not None else "nan"}')

        if not self.platform_tag_cache.is_valid(ttl):
            dns_tag = BasePlugin.parse_dns_tag(domain)
            if dns_tag:
                self.platform_tag_cache.set(dns_tag)
            else:
                # check if <meta/> tag exists with our tag
                header_tag = await BasePlugin.parse_meta_tag(content, meta_name)
                self.platform_tag_cache.set(header_tag)
        return self.platform_tag_cache.get()

    @staticmethod
    async def get_webpage_image_bytes(img_locator):
        """for playwright only"""
        b64 = await img_locator.evaluate(
            '(img) => {\
            img.crossOrigin="anonymous";\
            var canvas = document.createElement("canvas");\
            canvas.width = img.width;\
            canvas.height = img.height;\
            var ctx = canvas.getContext("2d");\
            ctx.drawImage(img, 0, 0);\
            var dataURL = canvas.toDataURL("image/png");\
            return dataURL;\
        }'
        )
        n = len("data:image/png;base64,")
        return base64.b64decode(b64[n:])

    # TODO: make this function more generic ( support bs4 too )
    # TODO: or maybe don't use bs4 at all?
    async def parse_links(self, page: Page):
        """gather all links on the page and yield them as subtasks. Only current domain urls are counted"""
        hrefs = await page.locator("a").all()
        for href_loc in hrefs:
            href = await href_loc.get_attribute("href")
            # logger.info(href)
            if href is not None:
                # logger.info( f'parse_link {href=} {type(href)=} {page.url} {type(page.url)=}')

                full_local_url = BasePlugin.get_local_url(href, page.url)
                # logger.info(full_local_url)
                if full_local_url:
                    # strict constraint on urls, else may get endless recursions etc
                    full_local_url = canonicalize_url(full_local_url)
                    # logger.info(full_local_url)

                    # logger.info( f'---------yielding {video_url=}')
                    yield CrawlerBackTask(url=full_local_url)
                    # logger.info( f'---------yielded {video_url=}')
                else:
                    # logger.info(f"non local: {href=} {page.url=}")
                    pass

    @staticmethod
    def get_text_storage_content(body: str, header: Optional[str] = None, excerpt: Optional[str] = None) -> str:
        data = (header + "\n" if header else "") + (excerpt + "\n" if excerpt else "") + body
        return data

    @staticmethod
    def gen_demo_tag(user_name):
        return "demo_" + md5(user_name.encode()).hexdigest()[-6:]

    @staticmethod
    async def parse_html_time_tag(page: Union[Page, Locator], loc: Optional[str] = "") -> int | None:
        """
        Works only with <time> html tag.
        Returns unix timestamp
        """
        res = None
        time_link = await page.locator(f"time{loc}").all()
        if len(time_link):
            dt = await time_link[0].get_attribute("datetime")
            if dt is not None:
                return BasePlugin.parse_datetime(dt)
        return res

    @staticmethod
    def parse_datetime(raw: str, fmt: Optional[str] = None) -> int:
        if fmt is None:
            parsed = date_parser.parse(raw).replace(tzinfo=None)
            epoch = datetime(1970, 1, 1, 0, 0, 0)
            return int((parsed - epoch).total_seconds())
        dt = datetime.strptime(raw, fmt)
        return calendar.timegm(dt.utctimetuple())


class BaseReader:
    @abstractmethod
    async def read_to(self, f: io.IOBase, stopper: Callable): ...


class BaseReaderException(Exception):
    pass


class ConnectionFailed(BaseReaderException):
    pass


class AuthFailed(BaseReaderException):
    pass


class ReadFailed(BaseReaderException):
    pass
