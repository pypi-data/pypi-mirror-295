import abc
import asyncio
import os
import sqlite3
import traceback
from typing import Any, Union

from telethon import errors
from telethon.errors import (AuthKeyDuplicatedError, AuthKeyUnregisteredError,
                             FloodError)
from telethon.extensions import markdown
from telethon.sessions import SQLiteSession, StringSession

from .telethon.client import PatchedTelegramClient
from .telethon.errors import patched_security_error_init
from .telethon.markdown import patched_parse
from .utils import AsyncDict, AsyncList, ShuttingDown, TGBotAbstractModel


class TelethonClientManager:
    proxys: Any
    timeout: int = 2
    try_limit: int = 5
    PARSE_CODE_LANG: bool = False
    SESSION_ROOT: str

    def __init__(
            self,
            number: Union[int, str],
            tgbots_list: list,
            responsible: bool,
            loop: asyncio.AbstractEventLoop,
            logger,
            send_msgs_for_update_client: callable,
            receive_updates: bool,
    ):
        asyncio.set_event_loop(loop)
        self.number = number
        self.tgbots_list = AsyncList(tgbots_list)
        self.responsible = responsible
        self.loop = loop
        self.logger = logger
        self.clients = AsyncDict()
        self.send_msgs_for_update_client = send_msgs_for_update_client
        self.receive_updates = receive_updates
        self.__telethon_patch()

    def __telethon_patch(self):
        if self.PARSE_CODE_LANG:
            # Патчим markdown для отображения кода, как в markdown_v2
            markdown.parse = patched_parse

        # Патчим SecurityError для log-сообщений
        errors.SecurityError.__init__ = patched_security_error_init

    async def _check_client(self, client):
        try:
            await client.get_me()
            return True
        except (Exception, BaseException) as exc:
            self.logger.check_client('error', exc)
            return False

    async def _get_or_create_session(
            self, username, session_name, str_session
    ):
        if str_session:
            return StringSession(str_session)
        session_username_dir = os.path.join(self.SESSION_ROOT, username)
        session_filename = f'{session_name}.session'
        session_path = os.path.join(session_username_dir, session_filename)
        os.makedirs(session_username_dir, exist_ok=True)
        return SQLiteSession(session_path)

    async def _delete_session(self, tgbot):
        session_name = (f'{tgbot.tgbot_id}_{self.number}'
                        if self.responsible else str(tgbot.tgbot_id))
        session_username_dir = os.path.join(self.SESSION_ROOT,
                                            tgbot.tg_username)
        session_filename = f'{session_name}.session'
        session_path = os.path.join(session_username_dir, session_filename)
        if os.path.exists(session_path):
            os.remove(session_path)
        else:
            self.logger.delete_session('info', f'{session_filename} not found')

    async def _get_client_info(self, tgbot_id) -> dict:
        for _ in range(self.try_limit):
            client_info = self.clients.get(
                tgbot_id) or self.clients.get(str(tgbot_id))
            if client_info is not None:
                return client_info
            else:
                await asyncio.sleep(self.timeout)
        raise KeyError(
            f'Client not found for {tgbot_id=}, {self.try_limit} tries.\n'
            f'{self.clients=}'
        )

    @abc.abstractmethod
    async def _get_str_session(self, tgbot):
        pass

    async def _wait_tgbot_update(self, tgbot_id):
        try_limit = 300  # 83 при последнем тесте понадобилось
        timeout = 1
        for attempt in range(try_limit):
            client_info = await self._get_client_info(tgbot_id)
            client_status = client_info.get('status')
            if client_status == 'ready':
                self.logger.wait_tgbot_update(
                    'error', f'{tgbot_id=}\n{attempt=}'
                )
                return
            await asyncio.sleep(timeout)
        msg = f'Failed to update tgbot {tgbot_id=}'
        self.logger.wait_tgbot_update('error', msg)
        raise RuntimeError(msg)

    async def _create_telegram_client(self, tgbot, str_session=False):
        """Creates telegram client"""
        if self.responsible:
            session_name = f'{tgbot.tgbot_id}_{self.number}'
        else:
            session_name = f'{tgbot.tgbot_id}'
        session = await self._get_or_create_session(
            tgbot.tg_username, session_name,
            str_session=str_session
        )
        api_id = tgbot.api_id
        api_hash = tgbot.api_hash
        proxy = self.proxys.get_new_proxy()
        bot_token = tgbot.api_key
        self.logger.create_telegram_client(
            'info', f'Started listener for tg_bot id={tgbot.tgbot_id}.'
        )
        return await PatchedTelegramClient(
            session, api_id, api_hash, loop=self.loop, proxy=proxy,
            receive_updates=self.receive_updates, custom_logger=self.logger,
        ).start(bot_token=bot_token)

    async def _safe_create_telegram_client(self, tgbot: TGBotAbstractModel):
        str_session = False
        for attempt in range(self.try_limit):
            msg = (f'{attempt=} to connect to telegram. {tgbot.tgbot_id=}, '
                   f'{self.responsible}, {self.number=}')
            try:
                return await self._create_telegram_client(tgbot, str_session)
            except sqlite3.OperationalError as exc:
                self.logger.create_telegram_client_sqlite3_error(
                    'error',
                    f'{msg}, error: {exc}, Traceback: {traceback.format_exc()}'
                )
                await self._delete_session(tgbot)
                await asyncio.sleep(self.timeout)
            except FloodError as exc:
                try:
                    seconds = exc.seconds
                except AttributeError:
                    seconds = self.timeout
                msg = f'Have to sleep {seconds} seconds. Error: {exc}'
                self.logger.flood_wait_error('error', msg)
                await asyncio.sleep(seconds)
            except Exception as exc:
                self.logger.try_create_telegram_client(
                    'error',
                    f'{msg}, error: {exc}, Traceback: {traceback.format_exc()}'
                )
                if attempt > 3 and not str_session:
                    str_session = self._get_str_session(tgbot)
                await self._delete_session(tgbot)
                await asyncio.sleep(self.timeout)

        msg = (f'Failed to create Telegram client after {self.try_limit} '
               f'retries.')
        self.logger.fatal_create_telegram_client('error', msg)
        raise RuntimeError(msg)

    def __dead_proxy_handler(self, client):
        self.logger.change_proxy('info', 'Changed proxy for client.')
        proxy = self.proxys.get_new_proxy()
        client.set_proxy(proxy)

    async def _run_client(self, client, tgbot):
        for attempt in range(self.try_limit):
            msg = f'{attempt=} to run client. '
            try:
                await client.start()
            except sqlite3.OperationalError as exc:
                self.logger.run_client_sqlite3_error('error', exc)
                await self.disconnect_client(client)
                client.session.close()
                client.session.delete()
                await self._delete_session(tgbot)
                return False
            except (AuthKeyDuplicatedError, AuthKeyUnregisteredError) as exc:
                self.logger.run_client_key_error('error', exc)
                await self.disconnect_client(client)
                await asyncio.sleep(self.timeout)
                return False
            except ConnectionError as exc:
                self.logger.connection_error('error', msg+str(exc))
                await self.disconnect_client(client)
                await asyncio.sleep(self.timeout)
            except Exception as exc:
                try:
                    self.logger.log_run_client_error('error', msg+str(exc))
                    await self.disconnect_client(client)
                    self.__dead_proxy_handler(client)
                    await asyncio.sleep(self.timeout)
                except sqlite3.OperationalError as exc:
                    self.logger.run_client_sqlite3_error('error', exc)
                    await self.disconnect_client(client)
                    client.session.close()
                    client.session.delete()
                    await self._delete_session(tgbot)
                    return False
            else:
                self.logger.log_run_client(
                    'info', f'Client {tgbot.tgbot_id=} is running. {attempt=}'
                )
                print('success !!!!!!!!!!!!!!!!!!!!')
                return True
        return False

    async def _end_client_session(self, tgbot_id: int):
        if tgbot_id in self.clients:
            self.clients[tgbot_id]['status'] = 'reconnecting'
            client = await self.get_client(tgbot_id, get_for_update=True)
            await self.disconnect_client(client)
            client.session.close()

    async def disconnect_client(self, client):
        is_connected = client.is_connected()
        if is_connected:
            await client.disconnect()
            self.logger.disconnect_client('info', f'{client=}')

    async def aio_stop(self):
        async for _, client_info in self.clients:
            client = client_info['client']
            await self.disconnect_client(client)
            client.session.close()
        self.logger.aio_stop(
            'error', f'Stopped {self.responsible=}, {self.number=}'
        )
        self.clients = AsyncDict()

    async def process_update_tgbot(
            self,
            tgbot_id: Union[int, TGBotAbstractModel],
            at_start: bool = False
    ) -> None:
        if isinstance(tgbot_id, ShuttingDown):
            await self.aio_stop()
            return
        for attempt in range(self.try_limit):
            if not at_start:
                tgbot = await self.get_tgbot_by_id(tgbot_id)
                if tgbot is None:
                    return
                await self._end_client_session(tgbot_id)
            else:
                tgbot = tgbot_id
                if tgbot.is_activated:
                    self.clients[tgbot.tgbot_id] = {
                        'client': None, 'status': 'reconnecting'
                    }
                else:
                    self.logger.process_update_tgbot(
                        'error', f'TGBot {tgbot_id=} was deactivated')
                    return
            client = await self._safe_create_telegram_client(tgbot)
            client_is_running = await self._run_client(client, tgbot)
            if not client_is_running or not await self._check_client(client):
                msg = f'Failed to run client {tgbot.tgbot_id=}, {attempt=}.'
                if attempt == self.try_limit - 1:
                    raise RuntimeError(msg)
                self.logger.process_update_tgbot('error', msg)
                continue
            self.clients[tgbot.tgbot_id] = {
                'client': client, 'status': 'ready'
            }
            self.logger.process_update_tgbot(
                'info', f'Client added {self.number}, {tgbot.tgbot_id}'
            )
            break

    async def reconnect_client(self, tgbot_id: int):
        client_info = await self._get_client_info(tgbot_id)
        if client_info['status'] == 'reconnecting':
            return
        if self.send_msgs_for_update_client is not None:
            self.logger.get_update_tgbot('info', f'Updated bot {tgbot_id=}.')
            await self.send_msgs_for_update_client(tgbot_id)

    async def run(self):
        async for tgbot in self.tgbots_list:
            await self.process_update_tgbot(tgbot, at_start=True)

    @abc.abstractmethod
    async def get_tgbot_by_id(self, tgbot_id: int) -> TGBotAbstractModel:
        pass

    async def get_client(self, tgbot_id, get_for_update=False):
        for attempt in range(self.try_limit):
            client_info = await self._get_client_info(tgbot_id)
            try:
                client_status = client_info['status']
                client = client_info['client']
                if get_for_update:
                    return client
                if client_status == 'reconnecting':
                    await self._wait_tgbot_update(tgbot_id)
                if not client.is_connected() or not await self._check_client(
                        client):
                    self.logger.get_client(
                        'error',
                        f'Client is not connected for {tgbot_id=}, {attempt=}.'
                    )
                    if attempt == 0:
                        await asyncio.sleep(self.timeout)
                    else:
                        await self.reconnect_client(tgbot_id)
                    continue
                self.logger.get_client('info', f'Client {tgbot_id} found.')
                return client
            except KeyError:
                self.logger.get_client(
                    'error' if attempt > 0 else 'info',
                    f'Invalid client id: {tgbot_id}, clients: '
                    f'{self.clients.keys()}, {client_info=}, {attempt=}.'
                )
                await asyncio.sleep(self.timeout)
        raise KeyError
