from typing import List,Optional
from pydantic import BaseModel
from datetime import datetime
from ..users.schemas import UserRequest,UserResponse
from ..category.schemas import CategoryRespone

#Expense Request
class ExpenseRequest(BaseModel):
    name: str
    amount: float
    remark: Optional[str] = None
    category_name : str

    class Config():
        orm_mode=True

#Expense Response
class ExpenseResponse(BaseModel):
    name: str
    amount: int
    remark: Optional[str] = ""
    user: UserResponse
    category: CategoryRespone

    class Config():
        orm_mode=True