from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime
from ..users.schemas import UserResponse

#Income Request
class IncomeRequest(BaseModel):
    classify: str
    amount: float
    class Config():
        orm_mode=True

#Update Income Request
class UpdateIncome(BaseModel):
    classify: Optional[str] = None
    amount: Optional[float] = None
    class Config():
        orm_mode=True

#Income Response
class IncomeResponse(BaseModel):
    id:int
    classify:str
    amount:float
    created_at: datetime
    updated_at:datetime
    user: UserResponse
    class Config():
        orm_mode=True