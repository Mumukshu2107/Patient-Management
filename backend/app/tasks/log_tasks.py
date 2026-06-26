import json

from app.queues.rabbitmq import get_channel


def send_log(log_data):

    connection, channel = get_channel(
        "log_queue"
    )

    channel.basic_publish(
        exchange="",
        routing_key="log_queue",
        body=json.dumps(log_data)
    )

    connection.close()