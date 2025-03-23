import pika
import json

RABBITMQ_HOST = "rabbitmq"  # Docker service name

def send_to_queue(message: dict):
    """Send a message to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue="product_queue", durable=True)

    # Publish message
    channel.basic_publish(
        exchange="",
        routing_key="product_queue",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),  # Persistent messages
    )

    print(f" [x] Sent {message}")
    connection.close()

def publish():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.basic_publish(
        exchange="",
        routing_key="product_queue",
        body="hello world",
    )