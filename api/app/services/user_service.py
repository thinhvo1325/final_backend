from cores.databases.db_helper import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from cores.sqlachemy_abstract.async_sqlachemy_abstract import SqlAchemyAbstract
from models.user_model import User
from cores.handler_response import handler_response


class UserService(SqlAchemyAbstract):
    _db = None
    def __init__(self, db: AsyncSession = Depends(get_db)) :
        self._db = db
        self.set_model(User)

    async def find_user(self, username, password):
        try:
            checker = await self.search(fields={'username': username, "password": password}, is_absolute=True)
            if checker is None:
                return handler_response(403, None, "Sai tài khoản hoặc mật khẩu")
            data = checker.__dict__
            data.pop('_sa_instance_state')
            import jwt
            payload = {'id': data['id'], 'email': data['email'], 'exp': 88125328211}
            return jwt.encode(payload, '22222', algorithm='HS256')
        except Exception as e:
            return handler_response(500, None, str(e))
        
    async def create_user(self, data: User, with_commit=True):
        try: 
            checker = await self.search(fields={'username': data.username}, is_absolute=True)
        
            if checker is not None:
                return handler_response(400, None, "User đã tồn tại")
            
            result = await super().create(data, with_commit)
            return handler_response(200, data, "Tạo user thành công")
        except Exception as e:
            return handler_response(500, None, str(e))
        
    
    async def update_user(self, username, password, data, with_commit=True):
        try:
            checker = await self.search(fields={'username': username, "password": password}, is_absolute=True)
            if checker is None:
                return handler_response(403, None, "Sai tài khoản hoặc mật khẩu")
            
            result = await super().update(id=checker.id, data=data, with_commit=with_commit)
            return handler_response(200, data, "Cập nhật user thành công")
        except Exception as e:
            return handler_response(500, None, str(e))
    

    async def delete_user(self, id, with_commit=True):
        try:
            checker = await self.find(id)
            if checker is None:
                return handler_response(404, None, "User không tồn tại")
            
            result = await super().delete(id, with_commit)
            return handler_response(200, result, "Xóa user thành công")
        except Exception as e:
            return handler_response(500, None, str(e))