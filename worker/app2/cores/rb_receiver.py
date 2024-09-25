import pika
from decouple import config
import json
from cores.model.predict_task import PredictTask

class RabbitMQReceiver(object):
    def __init__(self, queue_name=None, model_name=None):
        # super().__init__(model_name)
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.model = self._load_model(model_name)
    
    @staticmethod
    def _load_model(model_name):
        return PredictTask(model_name)
    
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
        print(body)
        if self.queue_name == 'object_detection':
            # service = ImportDownloadInfo()
            # service.import_download_info(body.decode('UTF-8'))
            self.model.predict(body['task_id'], json.loads(body['data'])['upload_result']['path'])
            ch.basic_ack(delivery_tag=method.delivery_tag)
        

        

    def start_consuming(self):
        self.connect()
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.close()




