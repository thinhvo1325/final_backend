from cores.databases.db_helper import Base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
class Image(Base):
    """
    Danh sách người dùng
    """
    __tablename__ = 'images'

    id = Column(Integer, nullable=False, primary_key=True)

    image_id = Column(String(100), nullable=False)
    phone_path = Column(String(100), nullable=True)
    resource_path = Column(String(13), nullable=True)
    status = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_date = Column(String(255), nullable=True) 
    object_list = Column(JSON, nullable=True)
    text_list = Column(String(10000), nullable=True)
    face_list = Column(JSON, nullable=True)
