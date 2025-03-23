import pika

RABBITMQ_HOST = "rabbitmq"

def callback(ch, method, properties, body):
    print(" [x] DjangoBackend Received %r" % body)

def consume():
    """Connect to RabbitMQ and start consuming messages."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue="product_queue", durable=True)

    channel.basic_consume(queue="product_queue", on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    consume()
