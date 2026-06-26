import json

from app.queues.rabbitmq import get_channel


def send_csv_task(file_path, entity):

    connection, channel = get_channel(
        "csv_queue"
    )

    channel.basic_publish(
        exchange="",
        routing_key="csv_queue",
        body=json.dumps({
            "file_path": file_path,
            "entity": entity
        })
    )

    connection.close()