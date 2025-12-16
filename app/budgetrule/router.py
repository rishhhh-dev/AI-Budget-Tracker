from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from .schemas import BudgetRequest,BudgetRespone
from ..utils import models
from ..utils.database import get_db
from ..users.token import get_current_user
from typing import List

router = APIRouter(
    prefix= '/api/budget',
    tags = ['Budget Rule']
)

#Get Rules
@router.get('/list',status_code=status.HTTP_200_OK,response_model=List[BudgetRespone],dependencies=[Depends(get_current_user)])
def get_rules(db:Session=Depends(get_db)):
    rules = db.query(models.BudgetRule).all()

    if not rules:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No rules defined yet")

    return rules

#Create Rule
@router.post('/create',status_code=status.HTTP_200_OK)
def create_rule(request:BudgetRequest,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    rule = db.query(models.BudgetRule).filter(models.BudgetRule.name == request.name).first()
    if rule:
        return {"detail":"Budget rule with name exists"}
    else:
        rule = models.BudgetRule(name=request.name,needs_percent=request.needs_percent,wants_percent=request.wants_percent,saving_percent=request.saving_percent,user_id=current_user.id)
        db.add(rule)
        db.commit()
        db.refresh(rule)

        return {"detail":{"budget":rule}}


#Update Rule
@router.put('/update/{name}',response_model=BudgetRespone,dependencies=[Depends(get_current_user)],status_code=status.HTTP_200_OK)
def update_rule(name:str,request:BudgetRequest,db:Session=Depends(get_db)):
    rule = db.query(models.BudgetRule).filter(models.BudgetRule.name == name).first()

    if not rule:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No rule with this name exists")
    
    rule.name = request.name
    rule.needs_percent = request.needs_percent
    rule.wants_percent = request.wants_percent
    rule.saving_percent = request.saving_percent
    db.commit()
    db.refresh(rule)

    return rule

#Delete Rule
@router.delete('/delete/{name}',dependencies=[Depends(get_current_user)],status_code=status.HTTP_200_OK)
def delete_rule(name:str,db:Session=Depends(get_db)):
    rule = db.query(models.BudgetRule).filter(models.BudgetRule.name == name).first()

    if not rule:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No rule with this name exists")
    
    db.delete(rule)
    db.commit()

    return {"detail":"Rule deleted"}