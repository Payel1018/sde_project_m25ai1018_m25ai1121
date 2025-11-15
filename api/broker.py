import json

import aio_pika
import pika


def publish_to_rabbitmq(queue_name: str, exchanger: str, routing_key: str, data: dict) -> None:
    # Connect to RabbitMQ (service name from docker compose)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    # Declare queue (idempotent)
    channel.queue_declare(queue=queue_name, durable=True)

    # Declare exchange (if needed)
    channel.exchange_declare(exchange=exchanger, exchange_type="direct", durable=True)

    # Bind queue to exchange
    channel.queue_bind(
        queue=queue_name,
        exchange=exchanger,
        routing_key=routing_key
    )

    # Publish
    channel.basic_publish(
        exchange=exchanger,
        routing_key=routing_key,
        body=json.dumps(data).encode(),
        properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
    )

    connection.close()


async def a_publish_to_rabbitmq(queue_name: str, exchanger: str, routing_key: str, data: dict) -> None:
    connection = await aio_pika.connect_robust(host="rabbitmq")
    channel = await connection.channel()
    exchange = await channel.get_exchange(exchanger)
    try:
        queue = await channel.get_queue(queue_name)
    except aio_pika.exceptions.ChannelNotFoundEntity:
        queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange, routing_key)
    message = aio_pika.Message(json.dumps(
        data).encode(), content_type="application/json")
    await exchange.publish(message, routing_key)
    await connection.close()
