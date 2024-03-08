from producer_interface import mqProducerInterface
import pika
import os

class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        self.routing_key = routing_key
        self.exchange_name = exchange_name

        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        connection = pika.BlockingConnection(parameters=con_params)
        self.channel = connection.channel()
        self.channel.exchange_declare(self.exchange_name)

    def publishOrder(self, message: str) -> None:
        message = 'Hi'
        self.channel.basic_publish(
            exchange=self.exchange_name, routing_key=self.routing_key, body=message)
        print(f" [x] Sent {self.routing_key}:{message}")