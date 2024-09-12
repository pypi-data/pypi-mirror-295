from telethon import errors
from tg_logger import BaseLogger

original_security_error_init = errors.SecurityError.__init__


def patched_security_error_init(self, *args):
    original_security_error_init(self, *args)
    exc_text = args[0] if args else ''
    if exc_text.startswith('Server replied with a wrong session ID'):
        logger = BaseLogger()
        logger.decrypt_message_data('error', exc_text)


class TelethonErrorHandler:
    @staticmethod
    def _get_tg_id(entity: 'hints.EntityLike', logger: BaseLogger) -> int:
        if isinstance(entity, int):
            return entity
        if hasattr(entity, 'user_id'):
            return int(entity.user_id)
        if hasattr(entity, 'id'):
            return int(entity.id)
        logger.get_tg_id('error', f'Could not get tg_id from {entity=}')
        return False

    @staticmethod
    async def set_sender_status(tg_id: int, client, status: str) -> None:
        pass

    @staticmethod
    async def get_sender_status(tg_id: int, client) -> None:
        pass

    @staticmethod
    def send_message_handler(func):
        async def wrapper(
                client: 'PatchedTelegramClient',
                entity: 'hints.EntityLike',
                *args,
                **kwargs
        ):
            logger = client.custom_logger
            try:
                return await func(client, entity, *args, **kwargs)
            except errors.InputUserDeactivatedError as exc:  # The specified user was deleted.
                tg_id = TelethonErrorHandler._get_tg_id(entity, logger)
                if tg_id:
                    await TelethonErrorHandler.set_sender_status(
                        tg_id, client, status='Deleted'
                    )
                logger.send_message(
                    'info', f'Sender {tg_id=} was deleted.{exc}'
                )
            except errors.EntityBoundsInvalidError as exc:  # There was an error parsing the message, we are trying to send it without parsing.
                logger.send_message(
                    'info',
                    f'Error occurred: {exc}\nTrying to send without parsing...'
                )
                initial_parse_mode = client.parse_mode
                client.parse_mode = None
                try:
                    return await func(client, entity, *args, **kwargs)
                finally:
                    client.parse_mode = initial_parse_mode
            except errors.UserBannedInChannelError as exc:  # you're banned from sending messages in supergroups/channels.
                msg = (f'You are banned from sending messages in '
                       f'supergroups/channels. {exc}')
                logger.send_message('error', msg)
            except errors.UserIsBlockedError as exc:  # User is blocked.
                tg_id = TelethonErrorHandler._get_tg_id(entity, logger)
                if tg_id:
                    await TelethonErrorHandler.set_sender_status(
                        tg_id, client, status='Banned'
                    )
                logger.send_message(
                    'info', f'Sender {tg_id=} blocked tgbot. {exc}'
                )
            except errors.BadRequestError as exc:  # The request was invalid or cannot be served.
                logger.send_message('error', f'Error occurred: {exc}')
                raise exc
            except errors.RPCError as exc:
                logger.send_message_rpce_error(
                    'error', f'Error occurred: {exc}'
                )
            except ValueError as exc:  # Could not find the input entity for PeerUser
                logger.send_message_value_error(
                    'error', f'Error occurred: {exc}'
                )
                tg_id = TelethonErrorHandler._get_tg_id(entity, logger)
                if not tg_id:
                    return
                try:
                    entity = await client.get_entity(tg_id)
                    return await func(client, entity, *args, **kwargs)
                except Exception as exc:
                    logger.send_message('error', f'Error occurred: {exc}')
                    await TelethonErrorHandler.set_sender_status(
                        tg_id, client, status='Banned'
                    )
        return wrapper
