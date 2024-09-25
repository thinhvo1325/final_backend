from pydantic import BaseModel
from typing import Optional

class LoginSchema(BaseModel):
    username: str
    password: str   

class UserCreateSchema(BaseModel):
    fullname: Optional[str]
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str]
    password: Optional[str]



class UserUpdateSchema(BaseModel):
    fullname: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
 
