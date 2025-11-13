import aio_pika

from logic import change_balance

QUEUE_NAME_TO_SECOND_SERVICE = "changebalance_orders"


async def start_consuming():
    connection = await aio_pika.connect(host="rabbitmq")
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME_TO_SECOND_SERVICE)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await change_balance(message)
