import json
import logging

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from mailer import send_welcome_email

logger = logging.getLogger(__name__)


def notify_user(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    data: bytes
):
    try:
        # 1. Decode message
        data = json.loads(data.decode())

        # 2. Extract fields
        email = data.get("email")
        user_id = data.get("user_id")
        name = data.get("name") or "User"         # optional
        role = data.get("role") or "customer"     # optional
        logger.warning(f"[AUTH EVENT] {email} ({user_id}) authenticated as {role}: EVENT CONSUMED")

        # 3. Send welcome email
        send_welcome_email(to=email, name=name)

        logger.warning(f"[*] Welcome email sent to {email}")

        # 4. Acknowledge the message
        #ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.error(f"Failed to process auth event: {e}")
        # Optionally: reject & requeue
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
