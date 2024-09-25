from cores.databases.db_helper import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    """
    Danh sách người dùng
    """
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    
    fullname = Column(String(100), nullable=False)
    phone = Column(String(13), nullable=True)
    address = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    username = Column(String(25), nullable=False)
    password = Column(String(255), nullable=False)
