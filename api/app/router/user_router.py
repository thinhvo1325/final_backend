from fastapi import APIRouter, Depends
from schemas.user_schemas import UserCreateSchema, UserUpdateSchema, LoginSchema
from services.user_service import UserService
from typing import Any
from cores.handler_response import response_return
router = APIRouter(
    prefix="/users",
    tags=['User'],
    responses={404: {"description": "Not found"}},
)



@router.post("/login")
async def login(
    obj: LoginSchema,
    user_service: UserService = Depends()
) -> Any:
    return await user_service.find_user(**obj.model_dump())

@router.post('/create')
async def create_users(
    obj: UserCreateSchema, 
    user_service: UserService = Depends()
) -> Any:
    result =  await user_service.create_user(obj)
    return response_return(**result)


@router.put("/update")
async def update_users(
    username: str,
    password: str,
    obj: UserUpdateSchema, 
    user_service: UserService = Depends()
) -> Any:
    result =  await user_service.update_user(username, password, obj)
    return response_return(**result)


@router.delete("/delete")
async def delete_users(
    id:int,
    user_service: UserService = Depends()
) -> Any:
    result =  await user_service.delete_user(id)
    return response_return(**result)
