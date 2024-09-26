from PIL import Image, ImageDraw
from decouple import config
from cores.model.model_loader.text_detection_loader import TextDetection
from cores.service_init import redis_connecter
from cores.rb_sender import RabbitMQSender
import pandas as pd
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
        model = TextDetection()
        return model
    
    def draw_image(self, file_path, list_text):
        image = Image.open(file_path)
        draw = ImageDraw.Draw(image)
        for detection in list_text:
            text, box = detection
            draw.polygon(box, outline="red", width=1)
            draw.text((box[0][0], box[0][1] - 10), text, fill="red")
        image.save(file_path.replace(config('FOLDER_UPLOAD'),config('FOLDER_TEXT')))


    def predict(self, task_id, file_path):
        try:
            data = self.model.predict(file_path)
            df = pd.DataFrame(data, columns=['text', 'bbox'])
            data_js = json.loads(df.to_json())

            text_detection_result = [{'text': data_js['text'][str(i)],
                    'bbox': data_js['bbox'][str(i)]}
                    for i in range(len(data))]
            # text_detection_result = [d['facial_area'] for d in data]
            status = json.loads(redis_connecter.get(task_id))
            status.update({'text_detection': text_detection_result})
            redis_connecter.set(task_id, json.dumps(status))
            self.sender.publish({'task_id': task_id, 
                                'type': 'text_detection',
                                'data': text_detection_result})
            self.draw_image(file_path, data)
        except Exception as e:
            return 
        