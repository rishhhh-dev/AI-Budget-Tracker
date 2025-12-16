from typing import List,Optional
from pydantic import BaseModel
from datetime import datetime
from ..users.schemas import UserResponse

#BudgetRule Request
class BudgetRequest(BaseModel):
    name : str
    needs_percent: int
    wants_percent : int
    saving_percent: int

    class Config():
        orm_mode=True

#BudgetRule Result
class BudgetRespone(BaseModel):
    id: int
    name: str
    needs_percent: int
    wants_percent : int
    saving_percent: int
    created_at: datetime
    user_id:int
    user: UserResponse
    class Config():
        orm_mode=True