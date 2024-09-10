import json
from abc import abstractmethod
from enum import Enum, IntEnum
from typing import Any, List, NamedTuple, Optional, TypeAlias, Union

from pydantic import AnyUrl, BaseModel
from pydantic_settings import BaseSettings

# from .storage import FileStorage

DEFAULT_WORKER_STUDY_URL_TASKS_R_QUEUE_NAME = "worker_study_url_queue_r"
DEFAULT_WORKER_STUDY_URL_TASKS_W_EXCHANGE_NAME = "worker_study_url_exchange_w"
DEFAULT_QUEUE_WORKER_HP_TASKS = "worker_hp_tasks"
# DEFAULT_QUEUE_WORKER_LP_TASKS = "worker_lp_tasks"
# DEFAULT_QUEUE_DELAYED_WORKER_TASKS = "delayed_worker_tasks"
DEFAULT_QUEUE_REPORTS = "worker_reports"
DEFAULT_QUEUE_EVAL_TASKS = "eval_tasks"
DEFAULT_STORAGE_INVALIDATION_EXCHANGE_NAME = "storage_invalidation_exchange"

DEFAULT_RABBITMQ_HOST = "rabbitmq.openlicense"
DEFAULT_RABBITMQ_PORT: int = 5672
DEFAULT_REDIS_HOST = "redis.openlicense"
DEFAULT_REDIS_PORT: int = 6379

DEFAULT_CONNECTION_URL: str = "amqp://guest:guest@{host}:{port}/".format(
    host=DEFAULT_RABBITMQ_HOST, port=DEFAULT_RABBITMQ_PORT
)

DEFAULT_BACKEND_API_URL: str = "https://openlicense.ai/internal/"
DEFAULT_BACKEND_HINTS_PERIOD: int = 10  # seconds

DEFAULT_MAX_STUDY_URL_PROCESSING_TASKS: int = 3
DEFAULT_MAX_PROCESSING_TASKS: int = 7

DEFAULT_MAX_TASKS_SLEEP: float = 3

# DEFAULT_STUDY_URL_TASK_WAIT_TIMEOUT: float = 3
# DEFAULT_HP_TASK_WAIT_TIMEOUT: float = 1
# DEFAULT_LP_TASK_WAIT_TIMEOUT: float = 0.2


class InvalidUsageException(Exception):
    pass


class BaseCrawlerSettings(BaseSettings):
    def fload(self, json_path):
        """fills self using json file path"""
        with open(json_path, "r") as fp:
            config = json.load(fp)  # expects dict output
            self.load(config)

    @abstractmethod
    def load(self, config: dict): ...


DONT_RETRY = -1


class SchedulerSettings(BaseCrawlerSettings):
    QUEUE_CONNECTION_URL: str = DEFAULT_CONNECTION_URL
    BACKEND_API_URL: str = DEFAULT_BACKEND_API_URL
    BACKEND_HINTS_PERIOD: int = DEFAULT_BACKEND_HINTS_PERIOD

    REDIS_HOST: str = DEFAULT_REDIS_HOST
    REDIS_PORT: int = DEFAULT_REDIS_PORT
    # cli settings
    CLI_MODE: bool = False

    WORKER_TASKS_QUEUE_NAME: str = DEFAULT_QUEUE_WORKER_HP_TASKS
    REPORTS_QUEUE_NAME: str = DEFAULT_QUEUE_REPORTS

    MAX_COMPLETE_TASKS: Optional[int] = None  # hard limit for faster testing
    MAX_EMPTY_COMPLETE_TASKS: Optional[int] = None

    def load(self, config: dict):
        """fills self with json config"""
        # Stop criteria
        stop_criteria = config.get("stop_criteria", {})
        self.MAX_EMPTY_COMPLETE_TASKS = stop_criteria.get("max_empty_complete_tasks")

        # Queue
        queue = config.get("queue", {})
        queue_connection_url = queue.get("connection_url")
        if queue_connection_url is not None:
            self.QUEUE_CONNECTION_URL = queue_connection_url

        self.WORKER_TASKS_QUEUE_NAME = queue.get("worker_tasks_queue_name", DEFAULT_QUEUE_WORKER_HP_TASKS)
        self.REPORTS_QUEUE_NAME = queue.get(
            "worker_reports_queue_name", DEFAULT_QUEUE_REPORTS
        )  # TODO: replace worker_reports_queue_name with reports_queue_name in config.json

        # Backend
        backend = config.get("backend", {})
        api_url = backend.get("api_url")
        if api_url is not None:
            self.BACKEND_API_URL = api_url
        hints_period = backend.get("hints_period")
        if hints_period is not None:
            self.BACKEND_HINTS_PERIOD = hints_period

        # Redis
        redis = config.get("redis", {})
        redis_host = redis.get("host")
        if redis_host is not None:
            self.REDIS_HOST = redis_host
        redis_port = redis.get("port")
        if redis_port is not None:
            self.REDIS_PORT = redis_port


class WorkerSettings(BaseCrawlerSettings):
    QUEUE_CONNECTION_URL: str = DEFAULT_CONNECTION_URL
    MAX_STUDY_URL_PROCESSING_TASKS: int = DEFAULT_MAX_STUDY_URL_PROCESSING_TASKS
    MAX_PROCESSING_TASKS: int = DEFAULT_MAX_PROCESSING_TASKS
    MAX_PLUGIN_INSTANCES_DEFAULT: int = 1
    MAX_TASKS_SLEEP: float = DEFAULT_MAX_TASKS_SLEEP
    # STUDY_URL_TASK_WAIT_TIMEOUT: float = DEFAULT_STUDY_URL_TASK_WAIT_TIMEOUT
    # HP_TASK_WAIT_TIMEOUT: float = DEFAULT_HP_TASK_WAIT_TIMEOUT
    # LP_TASK_WAIT_TIMEOUT: float = DEFAULT_LP_TASK_WAIT_TIMEOUT

    ATTEMPTS_PER_URL: int = 3
    ATTEMPTS_DELAY: int = 5  # seconds
    DELAYED_TASK_REDO_PERIOD: int = 20  # seconds
    STORAGE_PATH: str = "/storage/"

    REDIS_HOST: str = DEFAULT_REDIS_HOST
    REDIS_PORT: int = DEFAULT_REDIS_PORT

    WORKER_STUDY_URL_TASKS_R_QUEUE_NAME: str = DEFAULT_WORKER_STUDY_URL_TASKS_R_QUEUE_NAME
    WORKER_STUDY_URL_TASKS_W_EXCHANGE_NAME: str = DEFAULT_WORKER_STUDY_URL_TASKS_W_EXCHANGE_NAME
    WORKER_HP_TASKS_QUEUE_NAME: str = DEFAULT_QUEUE_WORKER_HP_TASKS
    # WORKER_LP_TASKS_QUEUE_NAME: str = DEFAULT_QUEUE_WORKER_LP_TASKS
    # DELAYED_WORKER_TASKS_QUEUE_NAME: str = DEFAULT_QUEUE_DELAYED_WORKER_TASKS
    REPORTS_QUEUE_NAME: str = DEFAULT_QUEUE_REPORTS
    EVAL_TASKS_QUEUE_NAME: str = DEFAULT_QUEUE_EVAL_TASKS
    STORAGE_INVALIDATION_EXCHANGE_NAME: str = DEFAULT_STORAGE_INVALIDATION_EXCHANGE_NAME
    TRUSTED_TAGS: Optional[List[str]] = None  # list of tags content of which will be parsed for priority_timestamp

    PUBLIC_DOMAINS: Optional[List[str]] = []

    # None: access is configured on AWS, bucket is NOT PUBLIC
    # "": bucket is PUBLIC
    # S3_IMAGESHACK_ACCESS_KEY: Optional[str] = None
    # S3_IMAGESHACK_ACCESS_SECRET: Optional[str] = None

    # GOOGLE_DRIVE_API_KEY: str = ""
    BACKEND_API_URL: str = DEFAULT_BACKEND_API_URL

    CLI_MODE: bool = False

    USE_ONLY_PLUGINS: Optional[List[str]] = None
    ADDITIONAL_PLUGINS: Optional[List[str]] = None
    ADDITIONAL_PLUGINS_DIR: Optional[str] = None

    plugins_config: dict = {}

    def load(self, config: dict):
        """fills self with json config"""

        # ====================
        # backend
        # ====================
        backend = config.get("backend", {})
        api_url = backend.get("api_url")
        if api_url is not None:
            self.BACKEND_API_URL = api_url

        # =====================
        # Queue
        # =====================
        queue = config.get("queue", {})
        queue_connection_url = queue.get("connection_url")
        if queue_connection_url is not None:
            self.QUEUE_CONNECTION_URL = queue_connection_url

        self.MAX_STUDY_URL_PROCESSING_TASKS = queue.get("max_study_url_tasks", DEFAULT_MAX_STUDY_URL_PROCESSING_TASKS)
        self.MAX_PROCESSING_TASKS = queue.get("max_hp_tasks", DEFAULT_MAX_PROCESSING_TASKS)
        self.MAX_TASKS_SLEEP = queue.get("max_tasks_sleep", DEFAULT_MAX_TASKS_SLEEP)
        # self.STUDY_URL_TASK_WAIT_TIMEOUT = queue.get("study_url_task_wait_timeout", DEFAULT_STUDY_URL_TASK_WAIT_TIMEOUT)
        # self.HP_TASK_WAIT_TIMEOUT = queue.get("hp_task_wait_timeout", DEFAULT_HP_TASK_WAIT_TIMEOUT)
        # self.LP_TASK_WAIT_TIMEOUT = queue.get("lp_task_wait_timeout", DEFAULT_LP_TASK_WAIT_TIMEOUT)

        self.WORKER_STUDY_URL_TASKS_R_QUEUE_NAME = queue.get(
            "worker_study_url_tasks_r_queue_name", DEFAULT_WORKER_STUDY_URL_TASKS_R_QUEUE_NAME
        )
        self.WORKER_STUDY_URL_TASKS_W_EXCHANGE_NAME = queue.get(
            "worker_study_url_tasks_w_exchange_name", DEFAULT_WORKER_STUDY_URL_TASKS_W_EXCHANGE_NAME
        )
        self.WORKER_HP_TASKS_QUEUE_NAME = queue.get("worker_hp_tasks_queue_name", DEFAULT_QUEUE_WORKER_HP_TASKS)
        # self.WORKER_LP_TASKS_QUEUE_NAME = queue.get("worker_lp_tasks_queue_name", DEFAULT_QUEUE_WORKER_LP_TASKS)
        self.REPORTS_QUEUE_NAME = queue.get(
            "worker_reports_queue_name", DEFAULT_QUEUE_REPORTS
        )  # replace worker_reports_queue_name with reports_queue_name in config.json
        self.EVAL_TASKS_QUEUE_NAME = queue.get("eval_tasks_queue_name", DEFAULT_QUEUE_EVAL_TASKS)
        self.STORAGE_INVALIDATION_EXCHANGE_NAME = queue.get(
            "storage_invalidation_queue_name", DEFAULT_STORAGE_INVALIDATION_EXCHANGE_NAME
        )

        # ====================
        # Redis
        # ====================
        redis = config.get("redis", {})
        redis_host = redis.get("host")
        if redis_host is not None:
            self.REDIS_HOST = redis_host
        redis_port = redis.get("port")
        if redis_port is not None:
            self.REDIS_PORT = redis_port

        # ====================
        # Storage
        # ====================
        storage = config.get("storage", {})
        worker_storage = storage.get("worker", {})
        storage_path = worker_storage.get("path")
        if storage_path is not None:
            self.STORAGE_PATH = storage_path

        # ====================
        # plugins
        # ====================
        self.plugins_config = config.get("plugins", {})

        # misc
        self.TRUSTED_TAGS = config.get("trusted_tags")
        self.PUBLIC_DOMAINS = config.get("public_domains", [])


class BaseProducerSettings(BaseCrawlerSettings):
    QUEUE_CONNECTION_URL: str = DEFAULT_CONNECTION_URL
    BACKEND_API_URL: str = DEFAULT_BACKEND_API_URL
    STORAGE_PATH: Optional[str] = None
    WORKER_STORAGE_PATH: str = "/worker_storage/"

    REDIS_HOST: str = DEFAULT_REDIS_HOST
    REDIS_PORT: int = DEFAULT_REDIS_PORT

    CLI_MODE: bool = False

    EVAL_TASKS_QUEUE_NAME: str = DEFAULT_QUEUE_EVAL_TASKS
    STORAGE_INVALIDATION_EXCHANGE_NAME: str = DEFAULT_STORAGE_INVALIDATION_EXCHANGE_NAME
    REPORTS_QUEUE_NAME: str = DEFAULT_QUEUE_REPORTS
    EMBEDDINGS_QUEUE_W_NAME: str = "embeddings_tasks_input_queue"
    EMBEDDINGS_EXCHANGE_R_NAME: str = "embeddings_tasks_output_exchange"

    def load(self, config: dict):
        """fills self with json config"""
        backend = config.get("backend", {})
        api_url = backend.get("api_url")
        if api_url is not None:
            self.BACKEND_API_URL = api_url

        # Queue
        queue = config.get("queue", {})
        queue_connection_url = queue.get("connection_url")
        if queue_connection_url is not None:
            self.QUEUE_CONNECTION_URL = queue_connection_url

        self.EVAL_TASKS_QUEUE_NAME = queue.get("eval_tasks_queue_name", DEFAULT_QUEUE_EVAL_TASKS)
        self.STORAGE_INVALIDATION_EXCHANGE_NAME = queue.get(
            "storage_invalidation_exchange_name", DEFAULT_STORAGE_INVALIDATION_EXCHANGE_NAME
        )

        # redis
        redis = config.get("redis", {})
        redis_host = redis.get("host")
        if redis_host is not None:
            self.REDIS_HOST = redis_host
        redis_port = redis.get("port")
        if redis_port is not None:
            self.REDIS_PORT = redis_port

        # Storage
        storage = config.get("storage", {})
        worker_storage = storage.get("worker", {})
        storage_path = worker_storage.get("path")
        if storage_path is not None:
            self.WORKER_STORAGE_PATH = storage_path
        producer_storage = storage.get("producer", {})
        storage_path = producer_storage.get("path")
        if storage_path is not None:
            self.STORAGE_PATH = storage_path


class CrawlerHintURLStatus(IntEnum):
    Unprocessed = 0
    Success = 1
    Failure = 2
    Processing = 3
    Rejected = 4
    Canceled = 5
    Restarted = 6
    UnPostponed = 7


class CrawlerHintURL(BaseModel):
    url: AnyUrl
    id: Optional[int] = 0
    status: Optional[CrawlerHintURLStatus] = CrawlerHintURLStatus.Unprocessed
    session_id: Optional[str] = None


class DatapoolContentType(str, Enum):
    Text = "Text"
    Image = "Image"
    Video = "Video"
    Audio = "Audio"

    def __hash__(self):
        if self.value == DatapoolContentType.Text:
            return 1
        if self.value == DatapoolContentType.Image:
            return 2
        if self.value == DatapoolContentType.Video:
            return 3
        if self.value == DatapoolContentType.Audio:
            return 4
        raise Exception(f"Not supported DatapoolContentType __hash__ {self.value}")


class BaseMessage(BaseModel):
    def to_dict(self):
        res = self.__dict__
        return res


class WorkerTask(BaseMessage):
    url: str
    content_type: Optional[DatapoolContentType] = None
    status: Optional[CrawlerHintURLStatus] = None


RequestIdType: TypeAlias = str
ReceiverRoutingKeyType: TypeAlias = str


class BaseChannelRequest(BaseMessage):
    request_id: RequestIdType
    receiver_routing_key: ReceiverRoutingKeyType


class BaseChannelResponse(BaseMessage):
    request_id: RequestIdType


class StudyUrlTask(BaseChannelRequest):
    url: str
    max_depth: int


class StudyUrlResponse(BaseChannelResponse):
    status: bool
    tags: Optional[List[str]] = None


class DomainType(IntEnum):
    Commercial = 1
    Public = 2
    Unlicensed = 3


class ProducerTask(BaseMessage):
    parent_url: str
    url: str
    worker_id: str
    storage_id: str
    content_key: str
    domain_type: DomainType
    tag_id: Optional[str] = None
    tag_keepout: Optional[bool] = False
    copyright_tag_id: Optional[str] = None
    copyright_tag_keepout: Optional[bool] = False
    platform_tag_id: Optional[str] = None
    platform_tag_keepout: Optional[bool] = False
    type: Optional[DatapoolContentType] = None
    priority_timestamp: Optional[int] = None


class DelayedWorkerTask(WorkerTask):
    timestamp: int


class EvaluationStatus(IntEnum):
    Success = 1
    Failure = 2


class SchedulerEvaluationReport(BaseMessage):
    status: EvaluationStatus


class WorkerEvaluationReport(BaseMessage):
    url: str
    storage_id: str
    is_shared_storage: bool
    session_id: str
    status: EvaluationStatus


class BaseCrawlerResult(BaseMessage):
    pass


class CrawlerContent(BaseCrawlerResult):
    tag_id: Optional[str] = None
    tag_keepout: Optional[bool] = False
    copyright_tag_id: Optional[str] = None
    copyright_tag_keepout: Optional[bool] = False
    platform_tag_id: Optional[str] = None
    platform_tag_keepout: Optional[bool] = False
    type: Optional[DatapoolContentType] = None
    # storage_id: Any
    url: Union[str, AnyUrl]
    download_url: Optional[Union[str, AnyUrl]] = None
    priority_timestamp: Optional[int] = None
    content: Optional[Any] = None
    content_key: Optional[str] = (
        None  # unique identifier of the content, used to distinguish between multiple contents on the same page
    )
    is_trusted_content: Optional[bool] = False

    def to_dict(self):
        res = self.__dict__
        res["type"] = res["type"].value
        return res


class CrawlerBackTask(BaseCrawlerResult):
    url: str


class CrawlerDemoUser(BaseCrawlerResult):
    user_name: str
    short_tag_id: str
    platform: str
    logo_url: Optional[str] = None


class CrawlerNop(BaseCrawlerResult):
    pass


class CrawlerPostponeSession(BaseCrawlerResult):
    pass
