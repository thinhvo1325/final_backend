from cores.databases.db_helper import Base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
class Imagedetail(Base):
    """
    Danh sách người dùng
    """
    __tablename__ = 'image_detail'

    image_id = Column(String(100), nullable=False)
    phone_path = Column(String(100), nullable=True)
    resource_path = Column(String(13), nullable=True)
    status = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_date = Column(String(255), nullable=True) 
