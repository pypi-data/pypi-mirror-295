import abc
import asyncio

from aio_rabbitmq import RabbitMQConnection, RabbitMQSettings
from tg_logger import BaseLogger


async def tg_request_with_retry(request_func, *args, **kwargs):
    from .settings import DEFAULT_REQUEST_RETRY_DELAYS
    logger = BaseLogger()
    for delay_count, delay in enumerate(DEFAULT_REQUEST_RETRY_DELAYS, 1):
        try:
            return await request_func(*args, **kwargs)
        except ConnectionError as exc:
            if delay_count == len(DEFAULT_REQUEST_RETRY_DELAYS):
                logger.error(
                    f'tg_request_with_retry: {request_func=}, {args=}, {exc}'
                )
                return
            await asyncio.sleep(delay)


def safe_get_loop() -> asyncio.AbstractEventLoop:
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError('Event loop is closed')
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


def configure_rabbitmq(
        rabbitmq_settings: RabbitMQSettings,
        logger: BaseLogger,
) -> RabbitMQConnection:
    return RabbitMQConnection(rabbitmq_settings, logger=logger)


class TGBotAbstractModel(abc.ABC):
    """
    Abstract class model of TGBot.
    """
    tgbot_id: int
    tg_username: str
    api_id: str
    api_hash: str
    api_key: str
    is_activated: bool


class ShuttingDown:
    """Class for Shutting Down Managers"""
    pass


class AsyncList(list):
    def __aiter__(self):
        return self._AsyncListIterator(self)

    class _AsyncListIterator:
        def __init__(self, async_list):
            self.list = async_list
            self.index = 0

        async def __aiter__(self):
            return self

        async def __anext__(self):
            if self.index < len(self.list):
                value = self.list[self.index]
                self.index += 1
                return value
            else:
                raise StopAsyncIteration


class AsyncDict(dict):
    def __aiter__(self):
        return self._AsyncDictIterator(self.items())

    class _AsyncDictIterator:
        def __init__(self, items):
            self.iterator = iter(items)

        async def __aiter__(self):
            return self

        async def __anext__(self):
            try:
                return next(self.iterator)
            except StopIteration:
                raise StopAsyncIteration
