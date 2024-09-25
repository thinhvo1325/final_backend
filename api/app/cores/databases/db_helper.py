#-----------------------------connect to database-----------------------------#
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
_host = config('MYSQL_HOST')
_username = config('MYSQL_ROOT_USERNAME')
_password = config('MYSQL_ROOT_PASSWORD')
_database = config('MYSQL_DATABASE')
# _database = 'test_collaborator'


async def get_db() -> AsyncSession:
    _engine = create_async_engine(
        f'mysql+asyncmy://{_username}:{_password}@{_host}/{_database}?charset=utf8mb4', echo=False, poolclass=NullPool,
        isolation_level="READ UNCOMMITTED")
    async_session = sessionmaker(autocommit=False, autoflush=False, bind=_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

#------------------------------create database-------------------------------#
from sqlalchemy_utils import database_exists, create_database, drop_database
def create_db(self):
    if database_exists(self._engine.url):
        drop_database(self._engine.url)

    create_database(self._engine.url, encoding='utf8mb4')
    self._engine.dispose(close=True)
    return database_exists(self._engine.url)            

#-------------------------------base model-----------------------------------#
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
