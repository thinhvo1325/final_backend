from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import uuid
import json
from cores import time_helper
from cores.service_init import redis_connecter
from cores.handle_upload import process_image_upload
from schemas.common_schemas import MlTimeHandle, ProccesStatus, DetectionResult, UploadResponse
from schemas.image_schemas import ImageFileSearchSchema, ImageUpdateSchema
from services.image_service import ImageService
from repositories.image_es_repo import ImageManager
from cores.handler_response import response_return
router = APIRouter(
    prefix="/image",
    tags=['Image'],
    responses={404: {"description": "Not found"}},
)
image_manager = ImageManager()  

@router.post("/upload")
async def upload(
    *,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks,
    image_service: ImageService = Depends()
):
    time = time_helper.now_utc()
    task_id = str(uuid.uuid4())
    time_handle = MlTimeHandle(start_upload=str(time.timestamp())).__dict__
    status_hanlde = ProccesStatus().__dict__
    data = DetectionResult(task_id=task_id, time=time_handle, status=status_hanlde)
    redis_connecter.set(task_id, json.dumps(data.__dict__))
    background_tasks.add_task(process_image_upload, await file.read(), task_id, time, data)
    await image_service.create({
        "image_id": task_id,
        "created_date": time,
        "status": 1,
        "user_id": 1})
    image_manager.insert_image(id=task_id, data={
        "image_id": task_id,
        "created_date": time,
        "is_public": False,
        "resource_path": None,
        "text_list": "",
        "face_embedding": [],
        "object_list": [],
        "user_id": 1})
    return UploadResponse(status="DETECTING", time=time, status_code=HTTP_200_OK, task_id=task_id)


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

@router.get("/list")
def get_list(
    *,
    page: int = 1, page_size: int = 10, 
    image_search_schemas: ImageFileSearchSchema = Depends(),
    is_search: bool = True
):
    result = image_manager.search(is_search=is_search, image_search_schemas=image_search_schemas.model_dump(), page=page, page_size=page_size)
    return result

@router.get("/cluster")
def get_cluster(
):
    result = image_manager.search( page_size=10000)
    list_cluser = {}
    list_link = {}
    for data in result['data']:
        if data.get('face_embedding') != []:
            for item in data.get('face_embedding'):
                if item['cluster'] not in list_cluser:
                    list_cluser[item['cluster']] = 0
                    list_link[item['cluster']] = ''
                list_cluser[item['cluster']] += 1
                list_link[item['cluster']] = 'http://160.30.112.24/upload' +data['resource_path']+'.jpg'
                


    if list_cluser.get(-1, None) is not None:
        del list_cluser[-1]
    if list_cluser.get(-5, None) is not None:
        del list_cluser[-5]
    return_list = [[k,v,list_link[k]] for k,v in list_cluser.items()]

    return return_list

@router.get("/cluster_image")
def get_cluster(cluser: int
):
    result = image_manager.search( image_search_schemas={'face_embedding.cluster': cluser}, page_size=10000)
    return result


@router.put('/update')
async def update_image(
    *,
    data: ImageUpdateSchema,
    image_service: ImageService = Depends()
):
    data = data.model_dump()
    image_ids = data.pop('image_id')
    data_update = {}
    for key, value in data.items():
        if value is not None:
            data_update[key] = value
    for id in image_ids:
        image_manager.update(id, data_update)
        await image_service.update(id, data_update, update_image=True)
    
    return response_return(code=200, message="Update success!", data=data)