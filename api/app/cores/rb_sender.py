import json
import pika
import pika
from decouple import config



class RabbitMQSender:
    def __init__(self, queue_name=None):
        self.queue_name = queue_name
        self._conn = None
        self._channel = None

    def connect(self):
        if not self._conn or self._conn.is_closed:
            credentials = pika.PlainCredentials(config('RABBITMQ_USER'), config('RABBITMQ_PASS'))
            parameters = pika.ConnectionParameters(config('RABBITMQ_HOST'),
                                                    9999,
                                                    '/',
                                                    credentials)

            self._conn = pika.BlockingConnection(parameters)
            self._channel = self._conn.channel()
            self._channel.queue_declare(queue=self.queue_name, durable=True)

    def close(self):
        if self._conn and self._conn.is_open:
            self._conn.close()

    def publish(self, message):
        self.connect()
        try:
            self._channel.basic_publish(
                exchange='', 
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
            )
        except Exception as e:
            raise e
        finally:
            self.close()

