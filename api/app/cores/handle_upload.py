
import datetime
import json
from decouple import config
# from fastapi import UploadFile
from schemas.common_schemas import DetectionResult
from cores import time_helper
from cores.file_helper import upload_file_bytes, create_path
from cores.service_init import redis_connecter, celery_execute
from cores.rb_sender import RabbitMQSender

async def process_image_upload(file_bytes, task_id: str, time: datetime, data: DetectionResult):
    file_name = task_id + ".jpg"
    dir_path = config('FOLDER_UPLOAD') +'/'+ time_helper.str_yyyy_mm_dd(time)    
    create_path(dir_path)
    file_path = dir_path + "/" +  file_name
    try:
        upload_file_bytes(file_bytes, file_path)
        # data.status['upload_id'] = task_id
        #update time
        data.time['end_upload'] = str(time_helper.now_utc().timestamp())

        #update status
        data.status['upload_status'] = "SUCCESS"
        data.status['detection_status'] = "DETECTING"

        #update upload result
        data.upload_result = {"path": file_path.replace(config('FOLDER_UPLOAD'), '')} 
        data_dump = json.dumps(data.__dict__)
        redis_connecter.set(task_id, data_dump)
        
        message = {
                'task_id': task_id,
                'data': data_dump,
        }
        #send task to queue
        #object detection
        RabbitMQSender(queue_name=config('QUEUE_OBJECT_DETECTION')).publish(message)
        RabbitMQSender(queue_name=config('QUEUE_TEXT_DETECTION')).publish(message)
        RabbitMQSender(queue_name=config('QUEUE_FACE_DETECTION')).publish(message)
    except Exception as e:
        data.status['upload_status'] = "FAILED"
        data.status['general_status'] = "FAILED"
        data.error = str(e)
        redis_connecter.set(task_id, json.dumps(data.__dict__))