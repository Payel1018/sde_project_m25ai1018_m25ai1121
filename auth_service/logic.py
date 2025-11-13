import json
import logging

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

logger = logging.getLogger(__name__)


def notify_user(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    data: bytes
):
    data = json.loads(data.decode())
    user = data.get("user_id")
    logger.warning(f"[*] - User with id {user} just notified. And subscribed")
