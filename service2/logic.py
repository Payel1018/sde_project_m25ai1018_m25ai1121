import json
import logging

from aio_pika import Message

logger = logging.getLogger(__name__)


async def change_balance(message: Message):
    """
    Logic service
    """
    async with message.process():
        data = json.loads(message.body.decode())
        user = data.get("user_id")
        logger.warning(
            f"[*] - User's balance with id {user} changed. Order checkouted")
