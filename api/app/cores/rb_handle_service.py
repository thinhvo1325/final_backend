from repositories.image_es_repo import ImageManager
from cores.service_init import redis_connecter
import json
import numpy as np
def get_centroid(box):
    return np.mean(box, axis=0)

def sort_word(data):
    sorted_words = sorted(data, key=lambda item: (get_centroid(item['bbox'])[1], get_centroid(item['bbox'])[0]))
    lines = []
    current_line = []

    current_y = None
    y_threshold = 5  

    for item in sorted_words:
        centroid_y = get_centroid(item['bbox'])[1]
        if current_y is None or abs(centroid_y - current_y) <= y_threshold:
            current_line.append(item)  
        else:
            lines.append(current_line)
            current_line = [item]
        current_y = centroid_y

    if current_line:
        lines.append(current_line)

    for line in lines:
        line.sort(key=lambda item: get_centroid(item['bbox'])[0])
    
    paragraphs = ''
    for i, line in enumerate(lines):
        paragraphs = paragraphs + ' ' + ' '.join([item['text'] for item in line])
    return paragraphs

class HandleImage():
    def __init__(self):
        self.image_manager = ImageManager()

    def update_iamge(self, body):
        task_id = body.get('task_id')
        detector = body.get('type')
        resource_path = json.loads(redis_connecter.get(task_id))['upload_result']['path']
        
        data = body.get('data')
        if detector == 'face_detection':
            for item in data:
                self.image_manager.update(task_id, {"face_embedding": item['embedding']})
        elif detector == 'object_detection':
            for item in data:
                item['score'] = float(item['score'])
                item['box'] = [float(x) for x in item['box'].strip('[]').split(', ')]
    
            self.image_manager.update(task_id, {"object_list": data, "resource_path": resource_path})
        elif detector == 'text_detection':
            self.image_manager.update(task_id, {"text_list": sort_word(data), "resource_path": resource_path})

