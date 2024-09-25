from fastapi import HTTPException, status, Depends, BackgroundTasks
from abc import ABCMeta, abstractmethod
from cores.sqlachemy_abstract.repository_contract import SqlAchemyContracts
from sqlalchemy.sql import func, update, delete
from sqlalchemy import asc, desc
from sqlalchemy.future import select
# from cores.logging import debug_logger


class SqlAchemyAbstract(SqlAchemyContracts):
    """Lớp tương tác với database thông qua sqlalchemy module"""
    __metaclass__ = ABCMeta
    _model = None

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        self._db = value

    @abstractmethod
    def get_model(self):
        return self._model

    @abstractmethod
    def set_model(self, model):
        """Khởi tạo model cho lớp"""
        self._model = model

    @abstractmethod
    def get_model(self):
        return self._model

    @abstractmethod
    async def get_all(self, with_trash: bool = False, options=[]):
        """Lấy tất cả records của bảng có trong self._db"""
        query = select(self._model).options(*options)
        if not with_trash:
            query = query.where(self._model.deleted_at.is_(None))

        executed = await self._db.execute(query)
        return executed.scalars().all()


    @abstractmethod
    async def find(self, id: int, with_trash: bool = False, options=[]):
        """Tìm kiếm record của bảng theo id"""

        # Kèm theo relationship và chế độ load
        query = select(self._model).where(
            self._model.id == id).options(*options)

        # Nếu with_trash=True thì lấy luôn các record đã bị xóa mềm
        if not with_trash and hasattr(self._model, 'deleted_at'):
            query = query.where(self._model.deleted_at.is_(None))
        executed = await self._db.execute(query)

        obj = executed.scalar()
        return obj


    @abstractmethod
    async def search_with_raw_query(self, query, is_get_first: bool = False, with_join: bool = False):
        executed = await self._db.execute(query)
        if with_join:
            return executed
        if is_get_first:
            return executed.scalar()
        return executed.scalars().all()
    
    @abstractmethod
    async def search(self, fields: dict = {}, order: dict = {}, is_absolute: bool = False, is_get_first=True,
                     options=[]):
        """Tìm kiếm 1 hoặc nhiều record theo điều kiện query trên bảng"""

        # Kèm theo relationship và chế độ load
        query = select(self._model).options(*options)

        """
            Nếu tồn tại ít nhất fields thì:
            - field là chuỗi thì thêm query khớp tương đối với chuỗi đã nhập
            - field là số thì thêm query khớp tuyệt đối với số đã nhập
            is_absolute=True: Tìm kiếm tuyệt đối
            is_absolute=False: Tìm kiếm tương đối
        """
        if fields:
            for k, v in fields.items():
                if v is not None:
                    if type(v) == int or type(v) == bool:
                        query = query.where(getattr(self._model, k) == v)
                    else:
                        v = v.strip()
                        if is_absolute:
                            query = query.where(
                                getattr(self._model, k).ilike(f'{v}'))
                        else:
                            query = query.where(
                                getattr(self._model, k).ilike(f'%{v}%'))
        if order:
            for k, v in order.items():
                if v == 'desc':
                    query = query.order_by(desc(getattr(self._model, k)))
                if v == 'asc':
                    query = query.order_by(asc(getattr(self._model, k)))

        executed = await self._db.execute(query)

        """
        is_get_first=True: Lấy 1 record
        is_get_first=False: Lấy nhiều record
        """
        if is_get_first:
            return executed.scalar()
        # if not obj:
        #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                         detail=f"Object is not available")
        return executed.scalars().all()

    @abstractmethod
    async def create(self, data, with_commit=True):
        """Thêm mới 1 record vào bảng"""

        if isinstance(data, self._model):
            pass
        else:
            # Convert data sang dict
            if type(data) is dict:
                data_to_dict = data
            else:
                data_to_dict = data.dict()

            # Parse dict sang sqlalchemy model
            data = self._model(**data_to_dict)

        try:
            """
            with_commit=False: Không commit sau khi thêm record
            with_commit=True: Commit sau khi thêm record
            """
            self._db.add(data)
            if with_commit:
                await self._db.commit()
                await self._db.refresh(data)
            else:
                await self._db.flush()

            return data
        except:
            await self._db.rollback()
            raise

    @abstractmethod
    async def update(self, id, data, with_restore: bool = False, with_commit=True, update_image: bool = False):
        """Cập nhật record theo id bảng"""
        # if not await self.find(self._db, id):
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                         detail=f"Object with the id: {id} is not available")
        try:
            # convert data sang dict
            if type(data) is not dict:
                data = data.dict()

            if update_image:
                q_obj = (update(self._model).where(self._model.image_id == id)
                     .values(data)
                     .execution_options(synchronize_session='fetch'))
            else:
                q_obj = (update(self._model).where(self._model.id == id)
                     .values(data)
                     .execution_options(synchronize_session='fetch'))
            executed = await self._db.execute(q_obj)

            """
            with_commit=False: Không commit sau khi cập nhật record
            with_commit=True: Commit sau khi cập nhật record
            """
            if with_commit:
                await self._db.commit()

            return await self.find(id)

        except Exception as e:
            print(e)
            await self._db.rollback()
            raise

    @abstractmethod
    async def delete(self, id, is_hard_delete: bool = False, with_commit=True):
        """Xóa record theo id bảng"""

        # Kiểm tra xem record với id đã nhập có tồn tại hay không
        if not await self.find(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Object with the id: {id} is not available")

        """
        is_hard_delete=True: Xóa cứng
        is_hard_delete=False: Xóa mềm
        """
        q_obj = (delete(self._model).where(self._model.id == id)
                    .execution_options(synchronize_session='fetch'))
        executed = await self._db.execute(q_obj)

        """
            with_commit=False: Không commit sau khi cập nhật record
            with_commit=True: Commit sau khi cập nhật record
        """
        if with_commit:
            await self._db.commit()
        # self._db.refresh(obj)

        return await self.search({'id': id})

    async def create_if_not_exist(self, fields: dict, data, is_absolute: bool = False, with_commit: bool = True):
        """Tìm kiếm record và tạo mới nếu không tồn tại"""

        search = await self.search(fields, is_absolute, is_get_first=True)

        if not search:
            return await self.create(data, with_commit=with_commit)

        return search
