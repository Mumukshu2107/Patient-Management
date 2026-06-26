import pika


def get_channel(queue_name):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost"
        )
    )

    channel = connection.channel()

    channel.queue_declare(
        queue=queue_name,
        durable=True
    )

    return connection, channel