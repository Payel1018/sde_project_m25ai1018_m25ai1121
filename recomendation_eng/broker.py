import pika
from logic import user_cart  # function that handles messages

# Queue and routing key
QUEUE_NAME = "user_cart"
EXCHANGE_NAME = "cart_exchange"  # example exchange
ROUTING_KEY = "user.cart"

def start_consuming():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()

    # Declare queue
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Optional: bind queue to exchange if using a direct/fanout exchange
    # channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct")
    # channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

    # Start consuming
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=user_cart,  # callback function
        auto_ack=True  # or set False and call ch.basic_ack inside callback
    )

    print(f"[*] Waiting for messages in queue '{QUEUE_NAME}'. To exit press CTRL+C")
    channel.start_consuming()
