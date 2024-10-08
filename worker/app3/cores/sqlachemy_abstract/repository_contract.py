from abc import ABCMeta, abstractmethod
class SqlAchemyContracts:
    __metaclass__ = ABCMeta
    @abstractmethod
    def find(self, db, id: int, with_trash: bool = False):
        pass

    @abstractmethod
    def get_by_user_id(self, db, user_id, is_get_first: bool = True, is_primary: bool = False, with_trash: bool = False, order='asc'):
        pass

    @abstractmethod
    def search(self, db, fields: dict = [], is_absolute: bool = False, is_get_first: bool = True):
        pass

    @abstractmethod
    def get_all(self, db, with_trash: bool = False):
        pass

    @abstractmethod
    def get_all_with_trash(self, db):
        pass

    @abstractmethod
    def paginate(self, db, params_pagination, params=None, with_trash: bool = False):
        pass

    @abstractmethod
    def paginate_with_trash(self, db, params):
        pass

    @abstractmethod
    def create(self, db, obj):
        pass

    @abstractmethod
    def update(self, db, id, obj, with_restore: bool = False):
        pass

    @abstractmethod
    def delete(self, db, id, is_hard_delete: bool = False):
        pass
