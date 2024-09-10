import asyncio
import io
from enum import IntEnum
import time
import importlib
import tempfile
import inspect
import os
import re
import sys
from pydantic import BaseModel
from cachetools import cached

# from ffmpeg import probe
# import ffmpeg

# ffmpeg.input("pipe:").output("aa.mp4").overwrite_output().run_async(pipe_stdin=True)

import traceback
import uuid
from typing import Optional, Set, List, Tuple, Any, Dict, NamedTuple, Union, Final

from ..common.backend_api import BackendAPI
from ..common.logger import logger
from ..common.queues import (
    GenericQueue,
    QueueMessage,
    QueueMessageType,
    QueueRole,
    QueueRoutedMessage,
    # MESSAGE_HINT_URL_PRIORITY,
)

from ..common.session_manager import SessionManager, Session, URLState, ContentStatus, ContentState, md5, SessionStatus
from ..common.stoppable import Stoppable
from ..common.storage import FileStorage
from ..common.types import (
    CrawlerBackTask,
    CrawlerContent,
    CrawlerDemoUser,
    CrawlerHintURLStatus,
    CrawlerNop,
    CrawlerPostponeSession,
    DatapoolContentType,
    InvalidUsageException,
    WorkerSettings,
    WorkerTask,
    DelayedWorkerTask,
    StudyUrlTask,
    StudyUrlResponse,
    WorkerEvaluationReport,
    ProducerTask,
    EvaluationStatus,
    DomainType,
)
from .types import WorkerContext, YieldResult
from .plugins.base_plugin import (
    BasePlugin,
    BaseTag,
    UnexpectedContentTypeException,
    DownloadFailureException,
    BaseReader,
    BaseReaderException,
    study_url_browser,
)
from .utils import get_worker_storage_invalidation_routing_key


class SessionFileStorage(FileStorage):
    def __init__(self, dstpath, session_id):
        super().__init__(os.path.join(dstpath, session_id))


class PluginData(NamedTuple):
    cls: Tuple[str, Any]
    lock: asyncio.Lock
    objs: List[BasePlugin]
    params: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None


class LoopResult(IntEnum):
    WorkerStopped = 1
    SessionClosed = 2
    PluginException = 3
    SessionPostponed = 4


MAX_INSTANCES_ERROR: Final[int] = -1


class ProcessTodoMessageResult(IntEnum):
    Skipped = 1
    Delayed = 2
    DelayedAgain = 3
    TryAgain = 4
    Done = 5


class TodoQueueData(BaseModel):
    queue: GenericQueue
    plugin_max_instances: Optional[int] = None
    reconfigured_prefetch_count: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True


class PluginRes(BaseModel):
    plugin: BasePlugin
    max_instances: Optional[int]

    class Config:
        arbitrary_types_allowed = True


class CrawlerWorker(Stoppable):
    id: str
    cfg: WorkerSettings
    demo_users: dict[str, dict[str, str]]
    api: BackendAPI
    session_manager: SessionManager
    st_todo_tasks: Set[asyncio.Task]
    todo_tasks: Set[asyncio.Task]
    plugins: List[PluginData]
    plugins_lock: asyncio.Lock
    st_todo_queue: GenericQueue
    st_response_queue: GenericQueue
    todo_queues: Dict[str, TodoQueueData]
    reports_queue: GenericQueue
    producer_queue: GenericQueue
    topics_queue: GenericQueue

    stop_task_received: Optional[asyncio.Event] = None

    def __init__(self, cfg: Optional[WorkerSettings] = None):
        super().__init__()
        self.id = uuid.uuid4().hex
        logger.info(f"worker id={self.id}")

        self.cfg = cfg if cfg is not None else WorkerSettings()

        self.demo_users = {}
        self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)

        self.session_manager = self._get_session_manager()

        self.st_todo_tasks = set()
        self.todo_tasks = set()

        self.plugins_lock = asyncio.Lock()
        self.plugins = []

        self.st_todo_queue = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.WORKER_STUDY_URL_TASKS_R_QUEUE_NAME,
            size=self.cfg.MAX_STUDY_URL_PROCESSING_TASKS,
        )
        logger.info(f"created receiver {self.cfg.WORKER_STUDY_URL_TASKS_R_QUEUE_NAME}")
        self.st_response_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=None,
            exchange_name=self.cfg.WORKER_STUDY_URL_TASKS_W_EXCHANGE_NAME,
        )
        logger.info(f"created publisher {self.cfg.WORKER_STUDY_URL_TASKS_W_EXCHANGE_NAME}")
        self.todo_queues = {}

        self.reports_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.REPORTS_QUEUE_NAME,
        )
        logger.info("created publisher reports")
        self.producer_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.EVAL_TASKS_QUEUE_NAME,
        )
        logger.info("created publisher eval_tasks")
        self.topics_queue = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=None,
            exchange_name=self.cfg.STORAGE_INVALIDATION_EXCHANGE_NAME,
            routing_key=get_worker_storage_invalidation_routing_key(self.id),
        )
        logger.info("created receiver topics")

        if self.cfg.CLI_MODE is True:
            self.stop_task_received = asyncio.Event()

    async def run(self):
        await study_url_browser.start()
        # self.tasks.append( asyncio.create_task( self.tasks_fetcher_loop() ) )
        await self.st_todo_queue.run()
        await self.st_response_queue.run()
        # await self.hp_todo_queue_r.run()
        # await self.lp_todo_queue_r.run()
        # await self.lp_todo_queue_w.run()
        await self.reports_queue.run()
        await self.producer_queue.run()
        await self.topics_queue.run()
        self.tasks.append(asyncio.create_task(self.study_loop()))
        self.tasks.append(asyncio.create_task(self.worker_loop()))
        self.tasks.append(asyncio.create_task(self.topics_loop()))
        await super().run()

    async def wait(self):
        """for CLI mode usage only"""
        if self.cfg.CLI_MODE is False:
            logger.error("worker invalid usage")
            raise InvalidUsageException("not a cli mode")
        logger.info("CrawlerWorker wait()")
        await self.stop_task_received.wait()
        logger.info("CrawlerWorker stop_task_received")
        waiters = [self.todo_queues[session_id].queue.until_empty() for session_id in self.todo_queues] + [
            self.st_todo_queue.until_empty(),
            self.st_response_queue.until_empty(),
            # self.hp_todo_queue_r.until_empty(),
            # self.lp_todo_queue_r.until_empty(),
            # self.lp_todo_queue_w.until_empty(),
            self.reports_queue.until_empty(),
            self.producer_queue.until_empty(),
            self.topics_queue.until_empty(),
        ]
        await asyncio.gather(*waiters)
        logger.info("CrawlerWorker wait done")

    async def stop(self):
        logger.info("worker::stop")
        await super().stop()
        logger.info("super stopped")

        logger.info("waiting todo tasks..")
        while len(self.st_todo_tasks) > 0 or len(self.todo_tasks) > 0:
            await asyncio.sleep(0.2)
        logger.info("todo tasks done")

        await self.st_todo_queue.stop()
        logger.info("st_todo queue stopped")
        await self.st_response_queue.stop()
        logger.info("st_response queue stopped")
        await asyncio.wait([self.todo_queues[session_id].queue.stop() for session_id in self.todo_queues])
        logger.info("todo queues stopped")
        # await self.lp_todo_queue_r.stop()
        # logger.info("lp_todo queue_r stopped")
        # await self.lp_todo_queue_w.stop()
        # logger.info("lp_todo queue_w stopped")
        await self.reports_queue.stop()
        logger.info("reports queue stopped")
        await self.producer_queue.stop()
        logger.info("producer queue stopped")
        await self.topics_queue.stop()
        logger.info("topics queue stopped")

        # for plugin_data in self.plugins:
        #     if plugin_data[0] is not None:
        #         logger.info( f'clearing plugin {plugin_data[1]}')
        #         plugin_data[0] = None
        #         plugin_data[1] = None

        logger.info("worker stopped")

    def _get_session_manager(self):
        return SessionManager(self.cfg.REDIS_HOST, self.cfg.REDIS_PORT)

    def _list_plugins(self, path: str, is_internal: bool):
        res = []
        if os.path.isdir(path):
            for dir_name in os.listdir(path):
                if dir_name != "__pycache__" and os.path.isdir(os.path.join(path, dir_name)):
                    if self.cfg.USE_ONLY_PLUGINS is None or dir_name in self.cfg.USE_ONLY_PLUGINS:
                        if is_internal:
                            name = f"datapools.worker.plugins.{dir_name}"
                        else:
                            name = dir_name
                        res.append(name)
        else:
            logger.error(f"Failed list plugins, not a directory {path}")
        return res

    async def init_plugins(self, reload_existing=False):
        plugin_names = []

        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
        logger.info(f"{plugins_dir=}")

        plugin_names += self._list_plugins(plugins_dir, True)
        if self.cfg.ADDITIONAL_PLUGINS_DIR is not None:
            logger.info(f"{self.cfg.ADDITIONAL_PLUGINS_DIR=}")
            plugin_names += self._list_plugins(self.cfg.ADDITIONAL_PLUGINS_DIR, False)

        if self.cfg.ADDITIONAL_PLUGINS is not None:
            for name in self.cfg.ADDITIONAL_PLUGINS:
                if importlib.util.find_spec(name):
                    plugin_names.append(name)

        logger.info(f"{sys.path=}")
        for name in plugin_names:
            reloaded = False
            try:
                if name not in sys.modules:
                    logger.info(f"loading module {name}")
                    module = importlib.import_module(name)
                elif reload_existing:
                    logger.info(f"RE-loading module {name}")
                    module = importlib.reload(sys.modules[name])
                    reloaded = True
                else:
                    logger.info(f"ignoring existing module {name}")
                    continue
            except ModuleNotFoundError:
                logger.error(f"Failed load module {name=}: not found")
                continue

            clsmembers = inspect.getmembers(module, inspect.isclass)

            async with self.plugins_lock:
                for cls in clsmembers:
                    # logger.info(f"{cls=}")
                    mro = inspect.getmro(cls[1])
                    # logger.info(f"{mro=}")

                    # logger.info(cls[1].__bases__)
                    for base in mro:  # cls[1].__bases__:
                        if base.__name__ == "BasePlugin":
                            logger.info(f"adding plugin {cls[0]}")
                            (params, config) = self._get_plugin_config_entry(cls[0])
                            plugin_data = PluginData(
                                cls=cls, lock=asyncio.Lock(), params=params, config=config, objs=[]
                            )
                            if reloaded is False:
                                self.plugins.append(plugin_data)
                            else:
                                for i in range(0, len(self.plugins)):
                                    if self.plugins[i].cls[0] == cls[0]:
                                        self.plugins[i] = plugin_data
                                        break
                            break

    async def topics_loop(self):
        # from Producer.Evaluator - receives storage_id which content can be removed
        try:
            while not await self.is_stopped():
                message = await self.topics_queue.pop(timeout=1)
                if message:
                    qm = QueueRoutedMessage.decode(message.routing_key, message.body)
                    logger.info(f"topics_loop {message.routing_key=}")

                    report = WorkerEvaluationReport(**qm.data)
                    logger.info(f"got producer {report=}")
                    if not report.is_shared_storage and report.status == EvaluationStatus.Success:
                        storage = SessionFileStorage(self.cfg.STORAGE_PATH, report.session_id)
                        await storage.remove(report.storage_id)

                    await self.topics_queue.mark_done(message)
        except Exception as e:
            logger.error(f"!!!!!!!!Exception in topics_loop() {e}")
            logger.error(traceback.format_exc())
        finally:
            logger.info("topics_loop done")

    async def study_loop(self):

        # fetches urls one by one from the queue and scans them using available plugins
        try:

            def on_done(task: asyncio.Task):

                logger.debug(f"_process_todo_message done {task=}")
                self.st_todo_tasks.discard(task)
                logger.debug(f"STUDY {len(self.st_todo_tasks)} still working")

            while not await self.is_stopped():
                # logger.info(f"worker_loop {label} iteration")
                if len(self.st_todo_tasks) < self.cfg.MAX_STUDY_URL_PROCESSING_TASKS:
                    message = await self.st_todo_queue.pop(timeout=3)
                    if message:
                        task = asyncio.create_task(
                            self._process_todo_message(message, is_delayable_on_max_instances=False)
                        )
                        task.add_done_callback(on_done)
                        self.st_todo_tasks.add(task)
                else:
                    await asyncio.wait(self.st_todo_tasks, timeout=3, return_when=asyncio.FIRST_COMPLETED)

        except Exception as e:
            logger.error(f"!!!!!!!!Exception in study_loop {e}")
            logger.error(traceback.format_exc())
        finally:
            logger.info("study_loop done")

    async def worker_loop(self):
        await self.init_plugins()
        # fetches urls one by one from random the queue and scans them using available plugins
        try:
            await self.session_manager.cleanup_active_sessions()

            def on_done(task: asyncio.Task):
                logger.debug(f"_process_todo_message done {task=}")
                self.todo_tasks.discard(task)
                logger.debug(f"{len(self.todo_tasks)} still working")

            last_queues_update = 0
            while not await self.is_stopped():
                # update active sessions list
                if time.time() - last_queues_update > 5:
                    last_queues_update = time.time()

                    session_ids = await self.session_manager.get_active_sessions()

                    # cleanup queues of non-active sessions
                    new_queues = {}
                    for session_id, data in self.todo_queues.items():
                        if session_id not in session_ids:
                            logger.info(f"stopping queue {data.queue.queue.queue_name}")
                            await data.queue.stop()
                            # await queue.delete()   scheduler should delete queue, not workers
                        else:
                            new_queues[session_id] = data
                    self.todo_queues = new_queues

                    # create new queues
                    for session_id in session_ids:
                        if session_id not in self.todo_queues:
                            await self._try_init_queue(session_id)

                if len(self.todo_queues) > 0:
                    if len(self.todo_tasks) < self.cfg.MAX_PROCESSING_TASKS:
                        # choose random input queue from the list
                        t = int(str(time.time()).split(".")[1])
                        i = t % len(self.todo_queues)
                        session_id = list(self.todo_queues.keys())[i]
                        # logger.info(f"reading queue for {session_id=} {t=}")

                        # check if prefetch_count is configured accordingly to plugin max_instances
                        if (
                            self.todo_queues[session_id].reconfigured_prefetch_count is False
                            and self.todo_queues[session_id].plugin_max_instances is not None
                            and self.todo_queues[session_id].plugin_max_instances
                            != 1  # try_init_queue sets size=1, so no reason to restart queue with the same param
                        ):
                            logger.info(
                                f"restarting queue with prefetch_count={self.todo_queues[session_id].plugin_max_instances}"
                            )
                            self.todo_queues[session_id].reconfigured_prefetch_count = True
                            # recreating queue, because there is no other way to change prefetch_count option
                            await self._try_init_queue(session_id, self.todo_queues[session_id].plugin_max_instances)

                        queue = self.todo_queues[session_id].queue

                        message = await queue.pop(timeout=0.1)
                        if message:
                            task = asyncio.create_task(
                                self._process_todo_message(message, is_delayable_on_max_instances=True)
                            )
                            task.add_done_callback(on_done)
                            self.todo_tasks.add(task)
                    else:
                        await asyncio.wait(self.todo_tasks, timeout=3, return_when=asyncio.FIRST_COMPLETED)
                else:
                    await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"!!!!!!!!Exception in study_loop {e}")
            logger.error(traceback.format_exc())
        finally:
            logger.info("study_loop done")

    async def loop_done(self, session: Session) -> LoopResult | None:
        if await self.is_stopped():
            return LoopResult.WorkerStopped
        if not await session.is_alive():
            return LoopResult.SessionClosed
        return None

    async def _process_todo_message(self, message, is_delayable_on_max_instances: bool) -> ProcessTodoMessageResult:

        heartbeat_stop: Optional[asyncio.Event] = None
        heartbeat_task: Optional[asyncio.Task] = None

        async def heartbeat(session_id):
            nonlocal heartbeat_stop
            try:
                name = asyncio.current_task().get_name()
                logger.debug(f"heartbeat task {name} started")
                sm = self._get_session_manager()  # separate redis connection
                session = await sm.get(session_id)

                while not heartbeat_stop.is_set():
                    await session.add_heartbeat(self.id)
                    await asyncio.sleep(1)
            except Exception:
                logger.error(f"Exception in heartbeat {name}")
                logger.error(traceback.format_exc())
            logger.debug(f"heartbeat task {name} finished")

        try:
            qm = QueueMessage.decode(message.body)

            task: Optional[Union[StudyUrlTask, WorkerTask]] = None

            if message.routing_key == self.cfg.WORKER_STUDY_URL_TASKS_R_QUEUE_NAME:
                task = StudyUrlTask(**qm.data)
                logger.info(f"study task {task.url=}")
                plugin_res = await self._get_url_plugin(task, ignore_max_instances=True)

                if plugin_res is None:
                    logger.info("suitable plugin not found")

                    await self.st_response_queue.push(
                        QueueRoutedMessage(
                            task.receiver_routing_key,
                            StudyUrlResponse(request_id=task.request_id, status=False),
                        )
                    )
                    await self._reject_message(message, requeue=False)
                    return ProcessTodoMessageResult.Skipped
                if isinstance(plugin_res, int):
                    raise Exception("not possible")

                plugin = plugin_res.plugin
                max_instances = plugin_res.max_instances

                logger.info(f"suitable {plugin=}")

                try:
                    study_res = await plugin.study(task)

                    await self.st_response_queue.push(
                        QueueRoutedMessage(
                            task.receiver_routing_key,
                            StudyUrlResponse(
                                request_id=task.request_id, status=True, tags=[str(tag) for tag in study_res]
                            ),  # TODO: does not matter t or n tag
                        )
                    )

                    logger.info(f"plugin.study done {study_res=}")
                except Exception:
                    logger.error("Exception in plugin.study")
                    logger.error(traceback.format_exc())
                    await self.st_response_queue.push(
                        QueueRoutedMessage(
                            task.receiver_routing_key,
                            StudyUrlResponse(request_id=task.request_id, status=False),
                        )
                    )

                await self._ack_message(message)
                plugin.is_busy = False

            elif qm.type in (QueueMessageType.Task, QueueMessageType.DelayedTask):
                session = await self.session_manager.get(qm.session_id)
                if not session or not await session.is_alive():
                    logger.error(f"Session not found or done {qm.session_id}")
                    await self._reject_message(message, qm.session_id, requeue=False)
                    return ProcessTodoMessageResult.Skipped

                # delaying tasks from a postponed session
                if await session.get_status() == SessionStatus.POSTPONED:
                    if qm.type == QueueMessageType.DelayedTask:
                        task = DelayedWorkerTask(**qm.data)
                        res = ProcessTodoMessageResult.DelayedAgain
                    else:
                        task = WorkerTask(**qm.data)
                        res = ProcessTodoMessageResult.Delayed
                    await self._add_delayed_task(qm.session_id, task, message)
                    return res

                # check timestamp of a delayed task
                if qm.type == QueueMessageType.DelayedTask:
                    delayed_task = DelayedWorkerTask(**qm.data)
                    diff = int(time.time()) - delayed_task.timestamp
                    # logger.info(f"delayed task time {diff=}")
                    if diff < self.cfg.DELAYED_TASK_REDO_PERIOD:
                        # it's not time to process this task, delay it again
                        await self._add_delayed_task(qm.session_id, delayed_task, message)
                        return ProcessTodoMessageResult.DelayedAgain

                task = WorkerTask(**qm.data)
                # logger.info(f"got {message=}")
                logger.info(f"got {task=} {qm.session_id=}")

                # # check if this message is not resent by rabbitmq as ack-timeouted
                # if message.redelivered is True:
                url_state = await session.get_url_state(task.url)
                if url_state is None:  # should not be possible because scheduler adds url
                    logger.error(f"url state not found for {task.url=}")
                    await self._reject_message(message, qm.session_id, requeue=False)
                    return ProcessTodoMessageResult.Skipped

                if url_state.status in (
                    CrawlerHintURLStatus.Success,
                    CrawlerHintURLStatus.Failure,
                    CrawlerHintURLStatus.Rejected,
                    CrawlerHintURLStatus.Canceled,
                ):
                    logger.error(f"url already processed: {task.url=} {url_state.status=} {url_state.worker_id=}")
                    await self._reject_message(message, qm.session_id, requeue=False)
                    return ProcessTodoMessageResult.Skipped

                if url_state.worker_id:
                    logger.info(f"{url_state.worker_id=}")
                    if url_state.worker_id == self.id:  # we are procesing this message already, ignoring
                        logger.info(f"already processing task {task.url=}, ignore")
                        await self._add_delayed_task(qm.session_id, task, message)
                        return ProcessTodoMessageResult.Delayed
                    if await self._is_worker_alive(url_state.worker_id, session):
                        logger.info(f"worker still alive on {task.url=}")
                        await self._add_delayed_task(qm.session_id, task, message)
                        return ProcessTodoMessageResult.Delayed
                    logger.info(f"it's dead, accepting task {task.url=}")

                # logger.info("setting url state")
                await session.set_url_state(
                    task.url, URLState(worker_id=self.id, status=CrawlerHintURLStatus.Processing)
                )
                # logger.info("creating heartbeat task")
                heartbeat_stop = asyncio.Event()
                heartbeat_task = asyncio.create_task(heartbeat(session.id))
                # logger.info("heartbeat task created")

                plugin_res = await self._get_url_plugin(task, session)

                if plugin_res is None:
                    logger.info("suitable plugin not found (2)")
                    await self._reject_message(message, qm.session_id, requeue=False)
                    return ProcessTodoMessageResult.Skipped

                if isinstance(plugin_res, int):
                    logger.debug(f"MAX_INSTANCES {session.id=}")
                    if is_delayable_on_max_instances:
                        await self._add_delayed_task(qm.session_id, task, message)
                        return ProcessTodoMessageResult.Delayed
                    else:
                        return ProcessTodoMessageResult.TryAgain

                plugin = plugin_res.plugin
                max_instances = plugin_res.max_instances

                # Later will update queue prefetch count accordingly to the plugin's max instances
                if max_instances is not None:
                    if self.todo_queues[qm.session_id].plugin_max_instances is None:
                        logger.info(f"{max_instances=}")
                        self.todo_queues[qm.session_id].plugin_max_instances = max_instances

                # logger.info(f"suitable {plugin=}")

                loop_result: LoopResult | None = None
                try:
                    n_contents_on_page = 0
                    n_contents_downloaded = 0
                    if plugin.is_allowed_by_robots_txt(task.url):
                        async for process_res in plugin.process(task):

                            loop_result = await self.loop_done(session)
                            if loop_result is not None:
                                if loop_result == LoopResult.SessionClosed:
                                    logger.info(f"Session is stopped/deleted, breaking. {qm.session_id=}")
                                elif loop_result == LoopResult.WorkerStopped:
                                    logger.debug("worker stopped, breaking")
                                break

                            if isinstance(process_res, CrawlerContent):
                                n_contents_on_page += 1
                                yield_result = await self._process_crawled_content(process_res, session, plugin, task)
                                if yield_result == YieldResult.ContentDownloadSuccess:
                                    n_contents_downloaded += 1
                            elif isinstance(process_res, CrawlerBackTask):
                                # url = plugin.ctx.real_task_url if plugin.ctx.real_task_url is not None else task.url
                                # if BasePlugin.is_sub_url(
                                #     url,
                                #     process_res.url,
                                # ):
                                if plugin.is_allowed_by_robots_txt(process_res.url):
                                    await self._add_back_task(qm.session_id, process_res)
                                else:
                                    logger.info(f"not allowed by robots.txt: {process_res.url}")
                                # else:
                                #     logger.info(f"{process_res.url} is not suburl of {url}")
                            elif isinstance(process_res, CrawlerDemoUser):
                                ct: CrawlerDemoUser = process_res
                                if ct.platform not in self.demo_users:
                                    self.demo_users[ct.platform] = {}
                                if ct.user_name not in self.demo_users[ct.platform]:
                                    logger.info(f"============= adding demo user {dict(ct)} ===========")
                                    await self.api.add_demo_user(dict(ct))
                                    self.demo_users[ct.platform][ct.user_name] = ct.short_tag_id

                            elif isinstance(process_res, CrawlerPostponeSession):
                                logger.info(f"postponing {session.id=}")

                                # if task is un-postponed session hint url
                                # then do not x2 postpone_duration if any content was downloaded in this loop
                                keep_postpone_duration = (
                                    task.status == CrawlerHintURLStatus.UnPostponed and n_contents_downloaded > 0
                                )
                                await session.postpone(keep_postpone_duration)
                                loop_result = LoopResult.SessionPostponed
                                break
                            elif isinstance(process_res, CrawlerNop):
                                pass
                            else:
                                raise Exception(f"unknown {process_res=}")

                            await self._notify_process_iteration(qm.session_id)
                        if n_contents_on_page == 0 and loop_result != LoopResult.SessionPostponed:
                            logger.debug("inc_since_last_tagged by empty page")
                            await session.inc_since_last_tagged()
                    else:
                        logger.info(f"not allowed by robots.txt {task.url}")

                except Exception:
                    logger.error("Exception in plugin loop")
                    logger.error(traceback.format_exc())
                    loop_result = LoopResult.PluginException

                # logger.info(f"plugin.process done {loop_result=}")

                plugin.is_busy = False

                if loop_result is None:  # task fully processed by plugin
                    logger.debug(f"sending ack for {message.message_id=}")
                    await self._ack_message(message, qm.session_id)
                    await session.set_url_status(task.url, CrawlerHintURLStatus.Success)
                    await self._report_task_status(session, task, CrawlerHintURLStatus.Success)
                elif loop_result == LoopResult.SessionPostponed:
                    logger.info(f"session is postponed {session.id=}")
                    await self._ack_message(message, qm.session_id)
                elif loop_result == LoopResult.SessionClosed:
                    logger.info("session closed")
                    await self._reject_message(message, qm.session_id, requeue=False)
                elif loop_result == LoopResult.WorkerStopped:
                    logger.info("worker stopped")
                    await self._reject_message(message, qm.session_id, requeue=True)
                elif loop_result == LoopResult.PluginException:
                    logger.debug(f"sending reject for {message.message_id=}")
                    await self._reject_message(message, qm.session_id, requeue=False)
                    await session.set_url_status(task.url, CrawlerHintURLStatus.Failure)
                    await self._report_task_status(session, task, CrawlerHintURLStatus.Failure)

            elif qm.type == QueueMessageType.Stop:
                if self.cfg.CLI_MODE is False:
                    logger.error("worker invalid usage")
                    raise InvalidUsageException("not a cli mode")
                await self._ack_message(message)
                logger.info("worker: got stop task")

                await self.producer_queue.push(
                    QueueMessage(session_id=qm.session_id, message_type=QueueMessageType.Stop)
                )
                # notifying scheduler that we are done
                await self.reports_queue.push(
                    QueueMessage(session_id=qm.session_id, message_type=QueueMessageType.Stop)
                )
                self.stop_task_received.set()  # type: ignore

            else:
                logger.error(f"!!!!!!!!!!!!!!! BUG: unexpected {message=} {qm=}")
                await self._reject_message(message, qm.session_id)
        except Exception:
            logger.error("unhandled exception in _process_todo_message")
            logger.error(traceback.format_exc())
            raise
        finally:
            if heartbeat_task is not None:
                logger.debug(f"waiting for heartbeat ends {heartbeat_task.get_name()}")
                heartbeat_stop.set()  # type: ignore
                await heartbeat_task
                logger.debug(f"heartbeat done {heartbeat_task.get_name()}")
            # logger.info("process_todo_message done ===============================")
        return ProcessTodoMessageResult.Done

    async def _ack_message(self, message, session_id: Optional[str] = None):
        if message.routing_key == self.cfg.WORKER_STUDY_URL_TASKS_R_QUEUE_NAME:
            await self.st_todo_queue.mark_done(message)
        elif session_id in self.todo_queues:
            await self.todo_queues[session_id].queue.mark_done(message)
        # elif message.routing_key == self.cfg.WORKER_LP_TASKS_QUEUE_NAME:
        #     await self.lp_todo_queue_r.mark_done(message)
        else:
            raise Exception(f"BUG: mark_done_message eunknown routing key {message=}")

    async def _reject_message(self, message, session_id: Optional[str] = None, requeue: Optional[bool] = True):
        if message.routing_key == self.cfg.WORKER_STUDY_URL_TASKS_R_QUEUE_NAME:
            await self.st_todo_queue.reject(message, requeue)
        elif session_id in self.todo_queues:
            await self.todo_queues[session_id].queue.reject(message, requeue)
        else:
            logger.warning(f"reject_message unknown routing key {message=}")

    async def _is_worker_alive(self, worker_id, session: Session):
        last_heartbeat = await session.get_heartbeat(worker_id)
        return time.time() - last_heartbeat < 60

    async def _report_task_status(self, session: Session, task: WorkerTask, status: CrawlerHintURLStatus):
        task.status = status
        await self.reports_queue.push(
            QueueMessage(session_id=session.id, message_type=QueueMessageType.ReportTaskStatus, data=task)
        )

    async def _notify_process_iteration(self, session_id):
        await self.reports_queue.push(
            QueueMessage(session_id=session_id, message_type=QueueMessageType.ProcessIteration)
        )

    @staticmethod
    def is_trusted_content(cfg: WorkerSettings, cc: CrawlerContent) -> bool:
        return cfg.TRUSTED_TAGS is not None and (
            (cc.platform_tag_id is not None and str(cc.platform_tag_id) in cfg.TRUSTED_TAGS)
            or (cc.copyright_tag_id is not None and str(cc.copyright_tag_id) in cfg.TRUSTED_TAGS)
            or (cc.tag_id is not None and str(cc.tag_id) in cfg.TRUSTED_TAGS)
        )

    async def _process_content_helper(
        self,
        cc: CrawlerContent,
        session: Session,
        url: str,
        storage: SessionFileStorage,
        storage_id: Optional[str] = None,
    ) -> bool:
        res = False
        # logger.info(f"process_content_helper {type(cc.content)=}")
        if cc.content:
            if not cc.type:
                try:
                    cc.type = BasePlugin.get_content_type_by_content(cc.content)
                except UnexpectedContentTypeException:
                    logger.error("Unsupported content, skipped")
            else:
                # plugin defined the content type - check if real type matches
                try:
                    content_type = BasePlugin.get_content_type_by_content(cc.content)
                    if content_type != cc.type:
                        logger.warning(f"content type mismatch: expected {cc.type}, got {content_type}")
                        return False

                except UnexpectedContentTypeException:
                    logger.error("Unsupported content, skipped")
                    return False

            # logger.info(f"{cc.type=}")

            if cc.type:
                if cc.type == DatapoolContentType.Text:
                    if not cc.tag_id:
                        # trying to parse author tag of TEXT
                        tag = BasePlugin.parse_content_tag(cc.content, cc.type)
                        if tag is not None:
                            logger.info(f"parsed author tag by content {cc.tag_id=} {cc.tag_keepout=}")
                            if tag != BaseTag(cc.copyright_tag_id, cc.copyright_tag_keepout) and tag != BaseTag(
                                cc.platform_tag_id, cc.platform_tag_keepout
                            ):
                                cc.tag_id = str(tag)
                                cc.tag_keepout = tag.is_keepout()
                else:
                    if not cc.copyright_tag_id or not cc.tag_id:
                        # trying to parse copyright/author tag of IMAGE,VIDEO,AUDIO metadata
                        tag = BasePlugin.parse_content_tag(cc.content, cc.type)
                        if tag is not None:
                            logger.info(f"parsed copyright/author tag by content {cc.tag_id=} {cc.tag_keepout=}")
                            if cc.copyright_tag_id is None:
                                if tag != BaseTag(cc.tag_id, cc.tag_keepout) and tag != BaseTag(
                                    cc.platform_tag_id, cc.platform_tag_keepout
                                ):
                                    cc.copyright_tag_id = str(tag)
                                    cc.copyright_tag_keepout = tag.is_keepout()
                            else:  # copyright tag was set already, then assume this is author tag
                                if tag != BaseTag(cc.copyright_tag_id, cc.copyright_tag_keepout) and tag != BaseTag(
                                    cc.platform_tag_id, cc.platform_tag_keepout
                                ):
                                    cc.tag_id = str(tag)
                                    cc.tag_keepout = tag.is_keepout()

                if True:  # supporting unlicensed content
                    # cc.tag_id is not None or cc.copyright_tag_id is not None or cc.platform_tag_id is not None:

                    if not cc.priority_timestamp:
                        # not parsing timestamp from content by default because it's possible way of cheating
                        if self.is_trusted_content(self.cfg, cc):
                            if cc.type == DatapoolContentType.Image:
                                cc.priority_timestamp = BasePlugin.parse_image_datetime(cc.content)
                            elif cc.type == DatapoolContentType.Audio:
                                cc.priority_timestamp = BasePlugin.parse_audio_datetime(cc.content)
                            elif cc.type == DatapoolContentType.Video:
                                cc.priority_timestamp = BasePlugin.parse_video_datetime(cc.content)

                        if cc.priority_timestamp:
                            logger.info(f"parsed content datetime by content {cc.priority_timestamp=}")

                    if storage_id is None:
                        storage_id = storage.gen_id(cc.content_key)
                        logger.info(f"putting to {storage_id=}")
                        await storage.put(storage_id, cc.content)

                        await session.set_content_state(
                            cc.content_key,  # type: ignore
                            ContentState(
                                worker_id=self.id, status=ContentStatus.DOWNLOAD_SUCCESS, storage_id=storage_id
                            ),
                        )
                        await session.inc_crawled_content()

                    if cc.tag_id is not None:
                        await session.inc_tag_usage(cc.tag_id, cc.tag_keepout)
                    if cc.copyright_tag_id is not None:
                        await session.inc_tag_usage(cc.copyright_tag_id, cc.copyright_tag_keepout)
                    if cc.platform_tag_id is not None:
                        await session.inc_tag_usage(cc.platform_tag_id, cc.platform_tag_keepout)

                    # notifying producer about new crawled data
                    producer_task = ProducerTask(
                        parent_url=url,
                        url=str(cc.url),
                        storage_id=storage_id,
                        tag_id=cc.tag_id,
                        tag_keepout=cc.tag_keepout,
                        copyright_tag_id=cc.copyright_tag_id,
                        copyright_tag_keepout=cc.copyright_tag_keepout,
                        platform_tag_id=cc.platform_tag_id,
                        platform_tag_keepout=cc.platform_tag_keepout,
                        type=DatapoolContentType(cc.type).value,
                        priority_timestamp=cc.priority_timestamp,
                        worker_id=self.id,
                        content_key=cc.content_key,  # type: ignore
                        domain_type=(
                            DomainType.Public
                            if self.is_public_domain(url)
                            else (
                                DomainType.Unlicensed
                                if cc.platform_tag_id is None and cc.copyright_tag_id is None and cc.tag_id is None
                                else DomainType.Commercial
                            )
                        ),
                    )
                    logger.info(f"sending producer task {producer_task=}")
                    await self.producer_queue.push(
                        QueueMessage(
                            session_id=session.id,
                            message_type=QueueMessageType.Task,
                            data=producer_task,
                        )
                    )
                    res = True
                else:
                    logger.info("no tag available")
            else:
                logger.info("unknown content type")
        else:
            logger.info("no content")

        return res

    async def _process_crawled_content(
        self, cc: CrawlerContent, session: Session, plugin: BasePlugin, task: WorkerTask
    ) -> YieldResult:
        is_content_tagged = False
        is_content_read = False
        is_content_ignored = False
        is_content_reused = False

        if not cc.content_key:
            cc.content_key = str(cc.url)
            # if cc.type == DatapoolContentType.Text and isinstance(cc.content, (str, bytes)):
            #     # multiple texts can be parsed on the same url, so make url "unique"
            #     content_hash = md5(cc.content)
            #     logger.info(f"text cc.content_key {str(cc.url)=} {content_hash=}")
            #     cc.content_key += "#" + content_hash

        content_state = await session.get_content_state(cc.content_key)
        # logger.info(f"_process_crawled_content {content_state=}")

        storage = SessionFileStorage(self.cfg.STORAGE_PATH, session.id)

        if content_state is None or (
            content_state.status in (ContentStatus.DOWNLOAD_SUCCESS, ContentStatus.EVALUATION_FAILURE)
            and (not content_state.storage_id or not await storage.has(content_state.storage_id))
        ):

            last_check = 0
            is_stopped = False

            async def stopper():
                nonlocal is_stopped
                if time.time() - last_check > 1:
                    is_stopped = await self.is_stopped() or not await session.is_alive()
                    return is_stopped
                return False

            if not cc.content:
                download_url = cc.url if cc.download_url is None else cc.url
                logger.info(f"no content, downloading from url {download_url=}")
                with tempfile.TemporaryFile("wb+") as tmp:
                    try:
                        async for chunk in plugin.async_read_url(download_url, expected_type=cc.type):
                            tmp.write(chunk)
                            if await stopper():
                                break
                        cc.content = tmp
                        is_content_read = True
                    except UnexpectedContentTypeException as e:
                        logger.error(f"Unexpected content type: {str(e)}")
                    except DownloadFailureException as e:
                        logger.error(f"Failed download: {str(e)}")

                    if is_content_read and not is_stopped:
                        if await self._process_content_helper(cc, session, task.url, storage):
                            is_content_tagged = True

            elif isinstance(cc.content, BaseReader):
                logger.debug("content is BaseReader instance")

                with tempfile.TemporaryFile("wb+") as tmp:
                    logger.info("read_to tmp")
                    try:
                        await cc.content.read_to(tmp, stopper)
                        is_content_read = True
                        logger.debug("read_to done")
                    except BaseReaderException as e:
                        logger.error(f"Reader failure: {e}")

                    if is_content_read and not is_stopped:
                        cc.content = tmp
                        if await self._process_content_helper(cc, session, task.url, storage):
                            is_content_tagged = True

            elif isinstance(cc.content, io.IOBase):
                logger.info("IOBase content")
                with tempfile.TemporaryFile("wb+") as tmp:
                    logger.info("read_to tmp")
                    try:
                        while not await stopper():
                            buf = cc.content.read(1024 * 1024)
                            if not buf:
                                break
                            tmp.write(buf)
                        is_content_read = True
                        logger.debug("write to tmp done")
                    except Exception as e:
                        logger.error(f"IOBase read failure: {e}")

                    if is_content_read and not is_stopped:
                        cc.content = tmp
                        if await self._process_content_helper(cc, session, task.url, storage):
                            is_content_tagged = True
            else:
                if await self._process_content_helper(cc, session, task.url, storage):
                    is_content_tagged = True

        elif content_state.status in (ContentStatus.DOWNLOAD_SUCCESS, ContentStatus.EVALUATION_FAILURE):
            is_content_reused = True

            # content was downloaded and put into storage, but not evaluated yet
            logger.info(f"content already downloaded for {cc.content_key=}")
            with storage.get_reader(content_state.storage_id) as r:
                cc.content = r
                if await self._process_content_helper(cc, session, task.url, storage, content_state.storage_id):
                    is_content_tagged = True

        elif content_state.status == ContentStatus.EVALUATION_SUCCESS:
            logger.info(f"content url evaluated already {cc.content_key=}")
            is_content_ignored = True
        elif content_state.status == ContentStatus.DOWNLOAD_INVALID:
            logger.info(f"content url downloaded earlier, but it's invalid {cc.content_key=}")
            is_content_ignored = True
        else:
            raise Exception(f"BUG: unknown status {content_state=}")

        # Stats for scheduler decision whether to continue crawling or not
        if is_content_ignored is False:
            if is_content_tagged is False:
                logger.debug("inc_since_last_tagged by crawled content")
                await session.inc_since_last_tagged()

                if is_content_read:  # content was downloaded but no tag found
                    await session.set_content_state(
                        cc.content_key,
                        ContentState(worker_id=self.id, status=ContentStatus.DOWNLOAD_INVALID),
                    )
            else:
                logger.info("reset_since_last_tagged")
                await session.update_meta({"since_last_tagged": 0})

            if is_content_read:
                plugin.ctx.yield_result = YieldResult.ContentDownloadSuccess
            elif is_content_reused:
                plugin.ctx.yield_result = YieldResult.ContentReused
            else:
                plugin.ctx.yield_result = YieldResult.ContentDownloadFailure

        else:
            plugin.ctx.yield_result = YieldResult.ContentIgnored
        # n = await session.get_since_last_tagged()
        # logger.info(f"get_since_last_tagged: {n}")
        return plugin.ctx.yield_result

    async def _add_back_task(self, session_id, task: CrawlerBackTask):
        logger.info(f"sending back task '{task.url=}' in '{session_id=}'")
        await self.reports_queue.push(
            QueueMessage(session_id=session_id, message_type=QueueMessageType.Task, data=task)
        )

    async def _try_init_queue(self, session_id, size: Optional[int] = None) -> GenericQueue:
        def create_queue():
            return GenericQueue(
                role=QueueRole.Both,
                url=self.cfg.QUEUE_CONNECTION_URL,
                name=f"{self.cfg.WORKER_HP_TASKS_QUEUE_NAME}_{session_id}",
                size=1 if size is None else size,
            )

        if size is None:
            if session_id not in self.todo_queues or size is not None:
                queue = create_queue()
                await queue.run()
                self.todo_queues[session_id] = TodoQueueData(queue=queue)
        else:  # recreating queue to set prefetch_count
            await self.todo_queues[session_id].queue.stop()
            queue = create_queue()
            await queue.run()
            self.todo_queues[session_id].queue = queue

        return self.todo_queues[session_id].queue

    async def _add_delayed_task(self, session_id, task: WorkerTask | DelayedWorkerTask, message):
        if type(task).__name__ == "WorkerTask":  # because of inheritance cannot use isinstance(task, WorkerTask)
            task = DelayedWorkerTask(**task.to_dict(), timestamp=int(time.time()))

        await self._ack_message(message, session_id)
        await self.todo_queues[session_id].queue.push(
            QueueMessage(session_id=session_id, message_type=QueueMessageType.DelayedTask, data=task)
        )

    def _get_plugin_object(self, cls, session: Optional[Session]) -> BasePlugin:
        ctx = WorkerContext(session=session)

        args = [ctx]
        kwargs = {}
        logger.debug(f"_get_plugin_object {cls=}")

        # convert class name into config plugins key
        # example: GoogleDrivePlugin => google_drive
        # example: S3Plugin => s3
        (params, __config) = self._get_plugin_config_entry(cls[0])
        if params is not None:
            # plugin config dict keys must match plugin's class __init__ arguments
            kwargs = params

        return cls[1](*args, **kwargs)

    def _get_plugin_config_entry(self, cls_name):
        cap_words = re.sub(r"([A-Z])", r" \1", cls_name).split()
        # logger.info(f'{cap_words=}')
        config_key = "_".join(list(map(lambda x: x.lower(), cap_words[:-1])))
        # logger.info(f'{config_key=}')
        config_entry = self.cfg.plugins_config.get(config_key)
        if config_entry is not None:
            # logger.info(config_entry)
            params = {k: v for k, v in config_entry.items() if k != "config"}
            config = config_entry.get("config")
            return (params, config)
        return (None, None)

    async def _get_url_plugin(
        self,
        task: WorkerTask | StudyUrlTask,
        session: Optional[Session] = None,
        ignore_max_instances: Optional[bool] = False,
    ) -> Optional[PluginRes] | int:

        def get_free_obj(plugin_data: PluginData):
            for obj in plugin_data.objs:
                if not obj.is_busy:
                    obj.ctx.session = session
                    return obj
            return None

        async with self.plugins_lock:
            for plugin_data in self.plugins:
                if plugin_data.cls[0] != "DefaultPlugin":
                    logger.debug(plugin_data.cls[0])
                    if plugin_data.cls[1].is_supported(task.url):
                        logger.debug(f"{plugin_data.cls[0]} supports {task.url}")
                        async with plugin_data.lock:
                            max_instances = None
                            if ignore_max_instances is False:
                                if plugin_data.config is not None:
                                    max_instances = plugin_data.config.get("max_instances")
                                if max_instances is None:
                                    max_instances = self.cfg.MAX_PLUGIN_INSTANCES_DEFAULT

                            logger.debug(f"{plugin_data.cls[0]} {max_instances=}")

                            obj = get_free_obj(plugin_data)
                            if obj is None:
                                if max_instances is not None:
                                    busy_count = plugin_data.cls[1].get_busy_count()
                                    logger.debug(f"{plugin_data.cls[0]} {busy_count=}")
                                    if busy_count >= max_instances:
                                        logger.debug(f"{plugin_data.cls[0]} max instances reached, {max_instances=}")
                                        return MAX_INSTANCES_ERROR

                                obj = self._get_plugin_object(plugin_data.cls, session)
                                obj.is_busy = True
                                plugin_data.objs.append(obj)
                            else:
                                obj.is_busy = True
                            logger.debug(f"returning {obj=}")
                            return PluginRes(plugin=obj, max_instances=max_instances)

            # creating/using existing default plugin
            for plugin_data in self.plugins:
                if plugin_data.cls[0] == "DefaultPlugin":
                    if plugin_data.cls[1].is_supported(task.url):
                        async with plugin_data.lock:
                            max_instances = None
                            if ignore_max_instances is False:
                                if plugin_data.config is not None:
                                    max_instances = plugin_data.config.get("max_instances")
                                if max_instances is None:
                                    max_instances = self.cfg.MAX_PLUGIN_INSTANCES_DEFAULT

                            obj = get_free_obj(plugin_data)
                            if obj is None:
                                if max_instances is not None:
                                    busy_count = plugin_data.cls[1].get_busy_count()
                                    if busy_count >= max_instances:
                                        logger.info(f"max instances reached, {max_instances=}")
                                        return MAX_INSTANCES_ERROR

                                obj = self._get_plugin_object(plugin_data.cls, session)
                                obj.is_busy = True
                                plugin_data.objs.append(obj)
                            else:
                                obj.is_busy = True
                            return PluginRes(plugin=obj, max_instances=max_instances)
                    break
        return None

    @cached(cache={})
    def is_public_domain(self, url):
        u = BasePlugin.parse_url(url)
        for domain in self.cfg.PUBLIC_DOMAINS:
            if BasePlugin.is_same_or_subdomain(u.netloc, domain):
                return True
        return False
