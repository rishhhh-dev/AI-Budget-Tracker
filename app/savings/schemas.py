from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
from ..users.schemas import UserResponse


#Request Saving
class SavingRequest(BaseModel):
    amount: float

#Response Saving
class SavingResponse(BaseModel):
    id:int
    amount:float
    created_at: datetime
    updated_at: datetime
    user: UserResponse