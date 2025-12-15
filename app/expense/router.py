from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from typing import Optional,List
from datetime import datetime,timedelta
from ..utils.database import get_db
from ..utils import models
from ..users.token import get_current_user
from .schemas import *

router = APIRouter(
    prefix='/api/expense',
    tags = ['Expense']
)

#Get Expense API
@router.get('/',response_model=List[ExpenseResponse],status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def expense_list(start_date:Optional[str]=None,end_date:Optional[str]=None,category:Optional[str]=None,db:Session=Depends(get_db)):


    if start_date and end_date:
        start = datetime.strptime(start_date,"%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        

        data = db.query(models.Expense).filter(models.Expense.created_at >= start,models.Expense.created_at <= end).all()


    elif category:
        category = db.query(models.Category).filter(models.Category.name == category).first()
       
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No category found")
        
        data = db.query(models.Expense).filter(models.Expense.category_id == category.id).all()
    
    else:
        data = db.query(models.Expense).all()
     

    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No expenses")
        
    return data


#Get Single Expense API
@router.get('/{id}',response_model=ExpenseResponse,status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def expense_list(id:int,db:Session=Depends(get_db)):

    data = db.query(models.Expense).filter(models.Expense.id == id).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No expense with this id exists")
    
    return data



#Create Expense API
@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_expense(request:ExpenseRequest,db:Session=Depends(get_db),current_user=Depends(get_current_user)):

    get_category = db.query(models.Category).filter(models.Category.id == request.category_id).first()
    
    if not get_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No category found')

    expense = models.Expense(name=request.name,amount=request.amount,remark=request.remark if request.remark else "",user_id=current_user.id,category_id=get_category.id)

    db.add(expense)
    db.commit()

    db.refresh(expense)

    return expense


#Update Expense API
@router.put('/update/{id}',status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def update_expense(id:int,name:str='',amount:int=0,db:Session=Depends(get_db)):

    expense = db.query(models.Expense).filter(models.Expense.id == id).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No expense exists with this id')

    if name != '':
        expense.name = name
    if amount > 0:
        expense.amount = amount
    
    expense.updated_at = datetime.now()

    db.commit()
    db.refresh(expense)

    return expense


#Delete Expense API
@router.delete('/delete/{id}',status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def delete_expense(id:int,db:Session=Depends(get_db)):
    
    expense = db.query(models.Expense).filter(models.Expense.id == id).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No expenses exists with this id")
    
    db.delete(expense)
    db.commit()

    return {"detail":{"expense deleted"}}