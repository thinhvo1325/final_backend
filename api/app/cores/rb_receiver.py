import pika
from decouple import config
import json
from cores.rb_handle_service import HandleImage

class RabbitMQReceiver(object):
    def __init__(self, queue_name=None, model_name=None):
        # super().__init__(model_name)
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        
    
    
    def connect(self):
        if not self.connection or self.connection.is_closed:
            credentials = pika.PlainCredentials(config('RABBITMQ_USER'), config('RABBITMQ_PASS'))
            parameters = pika.ConnectionParameters(config('RABBITMQ_HOST'),
                                                    9999,
                                                    '/',
                                                    credentials)

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True, auto_delete=False, exclusive=False)
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
            #self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def callback(self, ch, method, properties, body):
        body = json.loads(body)
        service = HandleImage()
        service.update_iamge(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.connect()
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.close()




