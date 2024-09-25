
from fastapi import APIRouter, status
from models import Base
from cores.databases.db_helper import get_db



router = APIRouter(
    prefix='/db',
    tags=['db'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.get('/create_tables/')
async def create_db():
    engine = await get_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@router.get('/delete_tables/')
async def create_db():
    engine = await get_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)