from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class MlTimeHandle(BaseModel):
    start_upload: str = None
    end_upload: str = None
    start_detection: str = None
    end_detection: str = None


class ProccesStatus(BaseModel):
    upload_status: str = "UPLOADING"
    detection_status: str = None


class DetectionResult(BaseModel):
    task_id: str
    status: dict = None
    time: dict = None
    upload_result: dict = None
    detection_draw_url: str = None
    error: Optional[str] = None
    
    
class UploadResponse(BaseModel):
    status: str = "DETECTING"
    status_code: int
    time: datetime
    task_id: str
    