from typing import List,Optional
from pydantic import BaseModel
from datetime import datetime
from ..expense.schemas import ExpenseRequest

#Category Request
class CategoryRequest(BaseModel):
    name : str
    class Config():
        orm_mode=True

#Category Result
class CategoryRespone(BaseModel):
    id: int
    name: str
    expense: List[ExpenseRequest] = []
    created_at: datetime
    updated_at: datetime
    class Config():
        orm_mode=True