from pydantic import BaseModel,EmailStr
from typing import List,Optional


class UserRequest(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

    class Config():
        orm_mode=True

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr

    class Config():
        orm_mode=True

class LoginRequest(BaseModel):
    email: str
    password: str

    class Config():
        orm_mode=True