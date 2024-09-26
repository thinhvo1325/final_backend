
from cores.model.model_loader.object_detection_loader import ObjectDetection
from cores.service_init import redis_connecter
from cores.rb_sender import RabbitMQSender
import json
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
        model = ObjectDetection()
        return model
    
    def predict(self, task_id, file_path):
        try:
            data = self.model.predict(file_path)
            object_detection_result = []
            for box, classes, score in zip(data['detection_boxes'], data['detection_classes'], data['detection_scores']):
                if score > 0.7:
                    object_detection_result.append({'box': str(list(box)), 'class': int(classes), 'score': str(round(score,3)*100)})
            status = json.loads(redis_connecter.get(task_id))
            status.update({'object_detection': object_detection_result})
            redis_connecter.set(task_id, json.dumps(status))
            self.sender.publish({'task_id': task_id, 
                                'type': 'object_detection',
                                'data': object_detection_result})
        except Exception as e:
            return
       
        