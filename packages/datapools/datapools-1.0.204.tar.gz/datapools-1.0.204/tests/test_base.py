from datapools.worker.plugins.base_plugin import BasePlugin, BaseTag
from datapools.worker.plugins.ftp import FTPPlugin
from datapools.worker.types import WorkerContext

from .fixtures import *


def test_tag_compare():
    t1 = BaseTag("asd", keepout=False)
    t2 = BaseTag("asd", keepout=False)
    assert t1 == t2

    t1 = BaseTag("asd", keepout=True)
    t2 = BaseTag("asd", keepout=True)
    assert t1 == t2

    t1 = BaseTag("asd", keepout=False)
    t2 = BaseTag("asd", keepout=True)
    assert t1 != t2

    t1 = BaseTag("asd", keepout=True)
    t2 = BaseTag("asd", keepout=False)
    assert t1 != t2

    t1 = BaseTag("asd", keepout=True)
    t2 = None
    assert t1 != t2

    t1 = None
    t2 = BaseTag("asd", keepout=True)
    assert t1 != t2

    t1 = BaseTag("asd", keepout=False)
    t2 = None
    assert t1 != t2

    t1 = None
    t2 = BaseTag("asd", keepout=False)
    assert t1 != t2


def test_tag_parsing():

    t = BasePlugin.parse_tag_in_str("\n https://openlicense.ai/asd")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/t/asd\nblabla")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("blabla openlicense.ai/t/asd \n")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("xopenlicense.ai/t/asd")
    assert t is None

    t = BasePlugin.parse_tag_in_str("\nhttps://openlicense.ai/n/asd blabla")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is True

    t = BasePlugin.parse_tag_in_str("openlicense.ai/n/asd blabla")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is True

    t = BasePlugin.parse_tag_in_str("xopenlicense.ai/n/asd")
    assert t is None

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/x/asd")
    assert t is None

    t = BasePlugin.parse_tag_in_str("openlicense.ai/x/asd")
    assert t is None


def test_ftp_link_parsing():
    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://user:password@host:21")
    assert user == "user"
    assert passwd == "password"
    assert host == "host"
    assert port == 21

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://host:21")
    assert user == "anonymous"
    assert passwd == ""
    assert host == "host"
    assert port == 21

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://user@host:22")
    assert user == "user"
    assert passwd == ""
    assert host == "host"
    assert port == 22

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://user@host")
    assert user == "user"
    assert passwd == ""
    assert host == "host"
    assert port == 21

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://host")
    assert user == "anonymous"
    assert passwd == ""
    assert host == "host"
    assert port == 21


def test_busy_count(session):
    class A(BasePlugin):
        @staticmethod
        def is_supported(url):
            return True

        async def process(self, task):
            pass

    class B(BasePlugin):
        @staticmethod
        def is_supported(url):
            return True

        async def process(self, task):
            pass

    ctx = WorkerContext(session=session)

    assert A.get_busy_count() == 0
    assert B.get_busy_count() == 0
    a = A(ctx)
    a.is_busy = True
    assert A.get_busy_count() == 1
    assert B.get_busy_count() == 0
    b = B(ctx)
    b.is_busy = True
    assert A.get_busy_count() == 1
    assert B.get_busy_count() == 1
    a.is_busy = False
    assert A.get_busy_count() == 0
    assert B.get_busy_count() == 1
    b.is_busy = False
    assert A.get_busy_count() == 0
    assert B.get_busy_count() == 0


def test_domains():
    assert BasePlugin.is_same_or_subdomain("bbc.m.wikipedia.org", "www.wikipedia.org") is True
    assert BasePlugin.is_same_or_subdomain("pl.m.wikipedia.org", "pl.wikipedia.org") is False


def test_date_parsing():
    assert BasePlugin.parse_datetime("1970-01-01") == 0
    assert BasePlugin.parse_datetime("1970:01:01", "%Y:%m:%d") == 0
    assert BasePlugin.parse_datetime("1970:01:01 00:00:05", "%Y:%m:%d %H:%M:%S") == 5
    assert BasePlugin.parse_datetime("1970", "%Y") == 0
    assert BasePlugin.parse_datetime("1970-02", "%Y-%M") == 120


def test_is_sub_url():
    assert BasePlugin.is_sub_url(
        "https://www.freepik.com/", "https://www.freepik.com/free-photo/beautiful-landscape-mother-nature_14958789.htm"
    )
    assert not BasePlugin.is_sub_url(
        "https://www.freepik.com/free-video",
        "https://www.freepik.com/free-photo/beautiful-landscape-mother-nature_14958789.htm",
    )

    assert BasePlugin.is_sub_url("ftp://user:pass@my.server:223", "/my/image.png")


def test_get_local_url():
    uri = "//imagizer.imageshack.com/v2/240x240q70/c/692/imgresoa.jpg"
    base = "https://imageshack.com"
    assert BasePlugin.get_local_url(uri, base) == f"https:{uri}"
