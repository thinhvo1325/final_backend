from cores.databases.db_helper import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from cores.sqlachemy_abstract.async_sqlachemy_abstract import SqlAchemyAbstract
from models.user_model import User


class UserService(SqlAchemyAbstract):
    _db = None
    def __init__(self, db: AsyncSession = Depends(get_db)) :
        self._db = db
        self.set_model(User)