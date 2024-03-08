import pika
import os
from consumer_interface import mqConsumerInterface

class mqConsumer(mqConsumerInterface):
    def __init__(self, binding_key: str, exchange_name: str, queue_name: str) -> None:
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.setupRMQConnection()
        
     
    def setupRMQConnection(self):
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue= self.queue_name)
        self.exchange = self.channel.exchange_declare(exchange= self.exchange_name)
        self.channel.queue_bind(
            queue= self.queue_name,
            routing_key= self.binding_key,
            exchange= self.exchange_name,
            )
        self.channel.basic_consume(
            self.queue_name, self.onMessageCallback, auto_ack=False
            )

    def onMessageCallback(self, channel, method_frame, header_frame, body):
        self.channel.basic_ack(method_frame.delivery_tag, False)
        print(body)
    
    def startConsuming(self):
        self.channel.start_consuming()
    
    def Del(self):
        self.channel.close()
        self.connection.close()