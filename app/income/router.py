from fastapi import HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .schemas import IncomeRequest,IncomeResponse,UpdateIncome
from ..utils import models
from ..utils.database import get_db
from ..users.token import get_current_user

router = APIRouter(
    prefix='/api/income',
    tags= ['Income']
)

#GET Request
@router.get('/list',status_code=status.HTTP_200_OK,response_model=List[IncomeResponse],dependencies=[Depends(get_current_user)])
def get_income(db:Session=Depends(get_db)):
    income = db.query(models.Income).all()
   
    if not income:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='No income added')
    
    return income

#GET Single Request
@router.get('/list/{classify}',status_code=status.HTTP_200_OK,response_model=IncomeResponse,dependencies=[Depends(get_current_user)])
def get_detail_income(classify:str,db:Session=Depends(get_db)):
    income = db.query(models.Income).filter(models.Income.classify == classify).first()

    if not income:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'No income found with this name {classify}')
    
    return income


#POST Request
@router.post('/create',status_code=status.HTTP_201_CREATED)
def create(request:IncomeRequest,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    income = db.query(models.Income).filter(models.Income.classify == request.classify).first()

    if income:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Income already exists with this name")
    
    new_income = models.Income(classify=request.classify,amount=request.amount,user_id=current_user.id)
    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return {"detail":{"income":new_income}}


#Update Request
@router.put('/update/{classify}',status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def update(classify:str,request:UpdateIncome,db:Session=Depends(get_db)):
    income = db.query(models.Income).filter(models.Income.classify == classify).first()

    if not income:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Income does not exists")
    print(request,"-=-======")
    
    income.classify = request.classify
    income.amount = request.amount
    income.updated_at = datetime.now()
    
    db.commit()
    db.refresh(income)

    return income

#Delete Request
@router.delete('/delete/{classify}',status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def delete(classify:str,db:Session=Depends(get_db)):
    income = db.query(models.Income).filter(models.Income.classify == classify).first()

    if not income:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='No income found')
    
    db.delete(income)
    db.commit()

    return {"detail":{"income deleted"}}