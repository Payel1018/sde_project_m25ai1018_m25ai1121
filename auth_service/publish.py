# auth_service/publish.py
import json
import pika
import aio_pika
import asyncio

RABBITMQ_HOST = "rabbitmq"  # Docker service name, same as your docker-compose

# ------------------------------
# Blocking (synchronous) publish
# ------------------------------
def publish_to_rabbitmq(queue_name: str, exchanger: str, routing_key: str, data: dict) -> None:
    """
    Publish a message to RabbitMQ (blocking).
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare exchange if it doesn't exist
    channel.exchange_declare(exchange=exchanger, exchange_type='topic', durable=False)

    # Declare queue if it doesn't exist
    channel.queue_declare(queue=queue_name, durable=True)

    # Bind queue to exchange
    channel.queue_bind(queue=queue_name, exchange=exchanger, routing_key=routing_key)

    # Publish message
    channel.basic_publish(
        exchange=exchanger,
        routing_key=routing_key,
        body=json.dumps(data).encode(),
        properties=pika.BasicProperties(content_type='application/json', delivery_mode=2)  # persistent
    )

    connection.close()

# ------------------------------
# Async publish using aio_pika
# ------------------------------
async def a_publish_to_rabbitmq(queue_name: str, exchanger: str, routing_key: str, data: dict) -> None:
    """
    Publish a message to RabbitMQ asynchronously.
    """
    connection = await aio_pika.connect_robust(host=RABBITMQ_HOST)
    channel = await connection.channel()

    # Declare exchange
    exchange = await channel.declare_exchange(exchanger, aio_pika.ExchangeType.DIRECT, durable=True)

    # Declare queue
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange, routing_key)

    # Create message
    message = aio_pika.Message(
        body=json.dumps(data).encode(),
        content_type="application/json",
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
    )

    # Publish
    await exchange.publish(message, routing_key=routing_key)

    await connection.close()

# Optional helper to run async publish in sync context
def run_async_publish(queue_name: str, exchanger: str, routing_key: str, data: dict):
    asyncio.run(a_publish_to_rabbitmq(queue_name, exchanger, routing_key, data))
