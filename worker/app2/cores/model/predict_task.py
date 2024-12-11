from PIL import Image, ImageDraw
import ast
from decouple import config
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
    
    def draw_image(self, file_path, list_object):
        image = Image.open(file_path)
        draw = ImageDraw.Draw(image)
        for obj in list_object:
            box = ast.literal_eval(obj["box"])
            x_min, y_min, x_max, y_max = box
            draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=1)
            label = f"Class {obj['class']}, {float(obj['score']):.2f}%"
            draw.text((x_min, y_min - 10), label, fill="red")
        image.save(file_path.replace(config('FOLDER_UPLOAD'),config('FOLDER_OBJECT')))


    def predict(self, task_id, file_path):
        try:
            data = self.model.predict(file_path)
            object_detection_result = data
            status = json.loads(redis_connecter.get(task_id))
            status.update({'object_detection': object_detection_result})
            # redis_connecter.set(task_id, json.dumps(status))
            self.sender.publish({'task_id': task_id, 
                                'type': 'object_detection',
                                'data': object_detection_result})
            self.draw_image(file_path, object_detection_result)
        except Exception as e:
            return
       
        