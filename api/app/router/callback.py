from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import uuid
import json
from cores import time_helper
from cores.service_init import redis_connecter
from cores.handle_upload import process_image_upload
from schemas.common_schemas import MlTimeHandle, ProccesStatus, DetectionResult, UploadResponse
from services.image_service import ImageService
router = APIRouter(
    prefix="/callback",
    tags=['Image'],
    responses={404: {"description": "Not found"}},
)


@router.get("/status/{task_id}")
def ml_status(
    *,
    task_id: str,
):
    data = redis_connecter.get(task_id)
    if data == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='task id not found!')
    message = json.loads(data)
    return message
