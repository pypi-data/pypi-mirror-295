import asyncio
import logging
import time
import traceback
from typing import List, Optional, Union
from urllib.parse import urlparse

import aio_pika
import aiormq
from httpx import AsyncClient
from pydantic import BaseModel

from ..logger import logger
from ..stoppable import Stoppable
from .types import QueueRole, QueueRoutedMessage, QueueMessage


class RestAPI:
    def __init__(self, connection_url):
        p = urlparse(connection_url)
        # TODO: port should be configurable
        self.url = f"http://{p.username}:{p.password}@{p.hostname}:15672/api/"

        logging.getLogger("httpx").setLevel(logging.WARNING)  # disable verbose logging when global level is INFO

    async def get_queue(self, queue_name):
        async with AsyncClient() as client:
            r = await client.get(f"{self.url}queues/%2f/{queue_name}")
            q = r.json()
            # print(q)
            return q


class RabbitmqParams(BaseModel):
    exchange_type: Optional[aio_pika.ExchangeType] = aio_pika.ExchangeType.DIRECT
    exchange_name: Optional[str] = None
    routing_key: Optional[Union[str, List[str]]] = None
    prefetch_count: Optional[int] = 1
    exclusive: Optional[bool] = False
    x_max_priority: Optional[int] = None


class RabbitmqQueue(Stoppable):
    connection: Optional[aio_pika.robust_connection.RobustConnection] = None
    channel: Optional[aio_pika.channel.Channel] = None
    queue_w: asyncio.Queue
    queue_r: asyncio.Queue
    queue_name: Optional[str]
    queue: Optional[aio_pika.queue.Queue] = None
    exchange_name: Optional[str]
    exchange: Optional[aio_pika.exchange.Exchange] = None
    _is_ready: bool

    def __init__(
        self,
        role: QueueRole,
        connection_url: str,
        queue_name: Optional[str] = None,
        params: Optional[RabbitmqParams] = RabbitmqParams(),
    ):
        super().__init__()
        self.role = role
        self.url = connection_url
        self.params = params
        self.queue_name = queue_name
        self.queue_w = asyncio.Queue()
        self.queue_r = asyncio.Queue()
        self.rest_api = RestAPI(self.url)
        self._is_ready = False

        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None

        # self.channel_invalid_state_flag = asyncio.Event()

    async def run(self):
        # logger.info( f'{id(self.role)=} {id(QueueRole.Receiver)=} {id(QueueRole.Publisher)=}' )
        self.tasks.append(asyncio.create_task(self.connection_keeper()))
        if self.is_producer():
            self.tasks.append(asyncio.create_task(self.publisher_loop()))
        if self.is_receiver():
            self.tasks.append(asyncio.create_task(self.receiver_loop()))
        await super().run()

    def is_producer(self):
        return self.role in (QueueRole.Publisher, QueueRole.Both)

    def is_receiver(self):
        return self.role in (QueueRole.Receiver, QueueRole.Both)

    async def stop(self):
        await super().stop()

    async def push(self, data):
        await self.push_w(data)

    async def pop(self, timeout=None):
        return await self.pop_r(timeout)

    async def push_w(self, data):
        await self.queue_w.put(data)

    async def push_r(self, data):
        await self.queue_r.put(data)

    async def pop_r(self, timeout=None) -> QueueMessage | None:
        return await self._pop(self.queue_r, timeout)

    async def pop_w(self, timeout=None) -> QueueMessage | None:
        return await self._pop(self.queue_w, timeout)

    async def _pop(self, queue, timeout):
        if timeout is None:
            # logger.info(f'rabbitmq pop {self.queue_name} no timeout')
            res = await queue.get()
            # logger.info(f'rabbitmq {self.queue_name} poped {res}')
            return res
        try:
            res = await asyncio.wait_for(queue.get(), timeout)
            return res
        except asyncio.TimeoutError:
            return None

    async def until_empty(self):
        last_log = 0
        while True:
            if self.queue_r.empty() and self.queue_w.empty():
                # if receiver then is receiver queue empty?
                if self.is_receiver():
                    queue = await self.rest_api.get_queue(self.queue_name)
                    if "message_stats" in queue:
                        if time.time() - last_log > 5:
                            last_log = time.time()
                            logger.info(
                                f'=================== receiver queue size {self.queue_name} {self.params} {queue["messages"]=} {queue["messages_unacknowledged"]=} {queue["message_stats"]["publish"]=} {queue["message_stats"]["deliver_get"]=}'
                            )
                        if (
                            queue["messages"] == 0
                            and queue["messages_unacknowledged"] == 0
                            # ensures that at least anything was put into and got out of the queue.
                            and queue["message_stats"]["publish"] > 0
                            and queue["message_stats"]["deliver_get"] >= queue["message_stats"]["publish"]
                        ):
                            break
                    elif queue["messages"] == 0 and "message_stats" not in queue:
                        # non touched queue => nothing to wait
                        break
                elif self.role == QueueRole.Publisher:
                    break
                else:
                    raise Exception("not implemented")
            await asyncio.sleep(1)

    async def mark_done(self, message: aio_pika.IncomingMessage):
        try:
            await message.ack()
        except aio_pika.exceptions.ChannelInvalidStateError:
            logger.error(f"ack for {message.message_id=} failed with ChannelInvalidStateError")
            # logger.error(f"{self.channel.is_closed=}")
            # self.channel_invalid_state_flag.set()

    async def reject(self, message: aio_pika.IncomingMessage, requeue: bool):
        try:
            await message.reject(requeue)
        except aio_pika.exceptions.ChannelInvalidStateError:
            logger.error(f"reject for {message.message_id=} failed with ChannelInvalidStateError")
            # logger.error(f"{self.channel.is_closed=}")
            # self.channel_invalid_state_flag.set()

    async def is_ready(self):
        return self._is_ready

    def _gen_queue_exchange_name(self):
        return f"{self.queue_name}_exchange"

    async def connection_keeper(self):
        try:
            while not await self.is_stopped(1):
                if self.channel and not self.channel.is_closed:
                    # logger.info("connection keeper: channel ok")
                    continue

                logger.info("creating connection")
                self._is_ready = False
                if self.channel is not None:
                    await self.channel.close()
                    self.channel = None

                if self.connection is not None:
                    await self.connection.close()
                    self.connection = None

                try:
                    self.connection = await aio_pika.connect_robust(self.url)
                except (aiormq.exceptions.AMQPConnectionError, StopAsyncIteration):
                    logger.info("Failed connect to rabbitmq, waiting..")
                    await asyncio.sleep(5)
                    continue

                logger.info("connected")

                self.channel = await self.connection.channel()
                logger.info(f"rabbitmq {self.queue_name} {self.channel=}")

                # Maximum message count which will be processing at the same time.
                if self.is_receiver():
                    await self.channel.set_qos(prefetch_count=self.params.prefetch_count)

                # Declaring queue
                arguments = {}
                if self.params.x_max_priority is not None:
                    arguments["x-max-priority"] = self.params.x_max_priority
                logger.info(f"creating queue {self.queue_name} {arguments=}")
                self.queue = await self.channel.declare_queue(
                    name=self.queue_name,
                    durable=True,
                    arguments=arguments,
                    exclusive=self.params.exclusive,
                )

                self.exchange_name = (
                    self.params.exchange_name
                    if self.params.exchange_name is not None
                    else self._gen_queue_exchange_name()
                )
                logger.info(f"creating exchange {self.exchange_name}")
                if self.params.exchange_type == aio_pika.ExchangeType.TOPIC:
                    self.exchange = await self.channel.declare_exchange(
                        name=self.exchange_name, type=aio_pika.ExchangeType.TOPIC, durable=True
                    )
                elif self.params.exchange_type == aio_pika.ExchangeType.DIRECT:
                    self.exchange = await self.channel.declare_exchange(
                        name=self.exchange_name, type=aio_pika.ExchangeType.DIRECT, durable=False
                    )
                else:
                    raise Exception(f"not supported {self.params.exchange_type=}")

                # bind queue even if it's only publisher: else if receiver is not started yet then immediately pushed message will be lost
                if self.queue_name or self.params.routing_key:
                    rks = (
                        self.params.routing_key
                        if isinstance(self.params.routing_key, list)
                        else [self.params.routing_key]
                    )
                    for rk in rks:
                        if rk == "":
                            rk = self.queue_name
                        logger.info(f"binding queue to {self.exchange_name=} {rk=}")
                        await self.queue.bind(self.exchange, routing_key=rk)

                self._is_ready = True
        except Exception as e:
            logger.error(f"Exception in connection_keeper() {e}, connection keeper stopped")
            logger.error(traceback.format_exc())

    async def publisher_loop(self):
        try:
            while not await self.is_stopped(1):
                if not self._is_ready:
                    continue

                # logger.info(f"rabbitmq {self.connection=} --------------------")
                try:
                    logger.info(f"rabbitmq {self.queue_name} publisher start")
                    while not await self.is_stopped():
                        if not await self.is_ready():
                            logger.info(f"channel for queue {self.queue_name} is closed, breaking publisher inner loop")
                            break
                        # logger.info( f'puslisher {self.queue_name} loop iteration')
                        message = await self.pop_w(1)
                        # logger.info( f'publisher loop {self.queue_name} poped {message=}')
                        if message is not None:
                            # logger.info(f"-------------------publishing msg {message.encode()}")

                            if isinstance(message, QueueRoutedMessage):
                                routing_key = message.routing_key
                            else:
                                routing_key = self.queue_name

                            # logger.info(f"publishing into {routing_key=} ")
                            await self.exchange.publish(
                                aio_pika.Message(
                                    body=message.encode(),
                                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                                    priority=message.priority,
                                ),
                                routing_key=routing_key,
                            )
                            # logger.info( f'published into {routing_key=}')

                            self.queue_w.task_done()
                    logger.info(f"rabbitmq {self.queue_name} publisher done")
                except Exception as e:
                    logger.error("exception in RabbitmqQueue::publisher_loop (internal)")
                    logger.error(traceback.format_exc())

        except Exception as e:
            logger.error("exception in RabbitmqQueue::publisher_loop, publisher stopped")
            logger.error(traceback.format_exc())

    async def receiver_loop(self):
        try:
            while not await self.is_stopped(1):
                if not await self.is_ready():
                    continue

                try:
                    logger.info(f"rabbitmq {self.queue_name} receiver start")

                    async with self.queue.iterator(timeout=3) as queue_iter:
                        while not await self.is_stopped():  # and not self.channel_invalid_state_flag.is_set():
                            if not await self.is_ready():
                                logger.info(
                                    f"channel for queue {self.queue_name} is closed, breaking receiver inner loop"
                                )
                                break
                            try:
                                message = await anext(queue_iter)
                                # logger.info(
                                #     f"receiver loop {self.queue_name=} {message.message_id=} {message.redelivered=} {message.delivery_tag=}"
                                # )
                                await self.push_r(message)
                                # logger.info(f"receiver pushed {message.message_id}")
                            except asyncio.TimeoutError:
                                pass

                    logger.info(f"rabbitmq {self.queue_name} consume done")

                except Exception as e:
                    logger.error(f"!!!!!!!!!!!!!!!!!! exception in rabbitmq receiver_loop(internal) {e}")
                    logger.error(traceback.format_exc())
        except Exception as e:
            logger.error(f"!!!!!!!!!!!!!!!!!! exception in rabbitmq receiver loop {e}, receiver stopped")
            logger.error(traceback.format_exc())

    async def delete(self):
        channel = await self.connection.channel()
        await channel.queue_delete(self.queue_name)
        await channel.exchange_delete(self.exchange_name)
