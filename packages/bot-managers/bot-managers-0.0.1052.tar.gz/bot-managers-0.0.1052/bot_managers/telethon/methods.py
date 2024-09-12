import asyncio

from telethon.client import MessageMethods, UploadMethods

from ..utils import tg_request_with_retry
from .errors import TelethonErrorHandler


class PatchedMessageMethods(MessageMethods):
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if callable(attr) and not name.startswith(
                '_') and asyncio.iscoroutinefunction(attr):
            async def wrapper(*args, **kwargs):
                return await tg_request_with_retry(attr, *args, **kwargs)
            return wrapper
        return attr

    @TelethonErrorHandler.send_message_handler
    async def send_message(self, *args, **kwargs):
        return await super().send_message(*args, **kwargs)

    @TelethonErrorHandler.send_message_handler
    async def safe_send_message(self, *args, **kwargs):
        sender_id = args[1]
        client = args[0]
        if isinstance(sender_id, int):
            sender_status = await TelethonErrorHandler.get_sender_status(
                sender_id, client)
            if sender_status in ['Deleted', 'Banned']:
                return
        return await super().send_message(*args, **kwargs)


class PatchedUploadMethods(UploadMethods):
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if callable(attr) and not name.startswith(
                '_') and asyncio.iscoroutinefunction(attr):
            async def wrapper(*args, **kwargs):
                return await tg_request_with_retry(attr, *args, **kwargs)
            return wrapper
        return attr

    @TelethonErrorHandler.send_message_handler
    async def send_file(self, *args, **kwargs):
        return await super().send_file(*args, **kwargs)

    @TelethonErrorHandler.send_message_handler
    async def safe_send_file(self, *args, **kwargs):
        sender_id = args[1]
        client = args[0]
        if isinstance(sender_id, int):
            sender_status = await TelethonErrorHandler.get_sender_status(
                sender_id, client)
            if sender_status in ['Deleted', 'Banned']:
                return
        return await super().send_file(*args, **kwargs)
