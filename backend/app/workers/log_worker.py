import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()
channel.basic_qos(prefetch_count=1)

channel.queue_declare(
    queue="log_queue",
    durable=True
)


def callback(ch, method, properties, body):

    data = json.loads(body)

    print("LOG:", data)


channel.basic_consume(
    queue="log_queue",
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for logs...")

channel.start_consuming()