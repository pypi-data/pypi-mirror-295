import asyncio
from typing import Union

from aio_rabbitmq import RabbitMQSettings
from tg_logger import BaseLogger

from .typing import ManagerType
from .utils import ShuttingDown, configure_rabbitmq, safe_get_loop


async def aio_update_tgbot(
        tgbot_id: Union[int, ShuttingDown],
        rabbitmq_settings: RabbitMQSettings,
        logger: BaseLogger,
        timeout: int = 2,
        expiration: int = 15,
        update_queue_name: str = 'update',
        type_manager: str = None
) -> None:
    from .settings import NUMBER_OF_MANAGERS
    loop = safe_get_loop()
    rabbitmq = configure_rabbitmq(rabbitmq_settings, logger, loop)
    channel = await rabbitmq.get_one_time_use_channel()
    if type_manager != ManagerType.RESPONSIBLE:
        name_manager = ManagerType.LISTENING
        if isinstance(tgbot_id, ShuttingDown):
            logger.update_tgbot(
                'info', f'Shutting down {name_manager}'
            )
        else:
            logger.update_tgbot(
                'info', f'Send msg for update {name_manager}, {tgbot_id=}'
            )
        await rabbitmq.send_message(
            f'{rabbitmq_settings.prefix}{update_queue_name}_{name_manager}',
            channel,
            tgbot_id,
            expiration=expiration,
        )
    if type_manager != ManagerType.LISTENING:
        for number in range(NUMBER_OF_MANAGERS):
            await asyncio.sleep(timeout)
            name_manager = f'{ManagerType.RESPONSIBLE}_{number}'
            if isinstance(tgbot_id, ShuttingDown):
                logger.update_tgbot(
                    'info', f'Shutting down {name_manager}'
                )
            else:
                logger.update_tgbot(
                    'info',
                    f'Send msg for update {name_manager}, {tgbot_id=}'
                )
            await rabbitmq.send_message(
                f'{rabbitmq_settings.prefix}{update_queue_name}_{name_manager}',
                channel,
                tgbot_id,
                expiration=expiration,
            )


def update_tgbot(
        tgbot_id: Union[int, ShuttingDown],
        rabbitmq_settings: RabbitMQSettings,
        logger: BaseLogger,
        timeout: int = 2,
        expiration: int = 15,
        update_queue_name: str = 'update',
        type_manager: str = None
):
    loop = safe_get_loop()
    loop.run_until_complete(
        aio_update_tgbot(
            tgbot_id, rabbitmq_settings, logger, timeout, expiration,
            update_queue_name, type_manager
        )
    )
