import pika

from logic import notify_user

QUEUE_NAME_TO_FIRST_SERVICE = "notify_user"


def connect_routes(channel):
    channel.basic_consume(QUEUE_NAME_TO_FIRST_SERVICE, notify_user)


def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(QUEUE_NAME_TO_FIRST_SERVICE)
    connect_routes(channel)
    channel.start_consuming()
