import pika

from logic import notify_user

QUEUE_NAME_TO_FIRST_SERVICE = "user_events"

QUEUE_NAME = "user_events"
EXCHANGE_NAME = "user_exchange"
ROUTING_KEY = "user.authenticated"

def connect_routes(channel):
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=notify_user,
        auto_ack=True,
    )

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()

    # 1. Declare exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic")

    # 2. Declare queue
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # 3. Bind queue to exchange
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=QUEUE_NAME,
        routing_key=ROUTING_KEY
    )

    # 4. Start consuming
    connect_routes(channel)
    channel.start_consuming()

