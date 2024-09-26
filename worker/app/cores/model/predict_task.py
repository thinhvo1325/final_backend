
from cores.model.model_loader.face_detection_loader import FaceDetection
from cores.service_init import redis_connecter
import json
from cores.rb_sender import RabbitMQSender
class PredictTask(object):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True
    model = None
    def __init__(self, model_name: str = None):
        self.model_name = model_name
        self.model = self.load_model()
        self.sender = RabbitMQSender('update_result')
    
    def load_model(self):
        model = FaceDetection()
        return model
    
    def predict(self, task_id, file_path):
        try:
            data = self.model.predict(file_path)
            text_detection_result = [d['facial_area'] for d in data]
            
            status = json.loads(redis_connecter.get(task_id))
            status.update({'face_detection': text_detection_result})
            redis_connecter.set(task_id, json.dumps(status))
            self.sender.publish({'task_id': task_id, 
                                'type': 'face_detection',
                                'data': data})
        except Exception as e:
            return
       