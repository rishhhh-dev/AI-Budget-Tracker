from typing import List,Optional
from pydantic import BaseModel
from datetime import datetime
from ..users.schemas import UserResponse

class WishlistRequest(BaseModel):
    name: str
    budget: float
    goal: str
    
    class Config():
        orm_mode=True
    

class WishlistResponse(BaseModel):
    name: str
    budget: float
    goal: str
    created_at: datetime
    updated_at: datetime

    user: UserResponse

    class Config():
        orm_mode=True