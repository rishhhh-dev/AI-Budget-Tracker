from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from datetime import datetime
from .schemas import SavingRequest,SavingResponse
from typing import List
from ..users.token import get_current_user
from ..utils import models
from ..utils.database import get_db


router = APIRouter(
    prefix = '/api/saving',
    tags = ['Saving']
)


#GET Request
@router.get('/list',status_code=status.HTTP_200_OK,response_model=List[SavingResponse],dependencies=[Depends(get_current_user)])
def get_savings(db:Session=Depends(get_db)):
    query = db.query(models.Saving).all()

    if not query:
        raise HTTPException(sattus_code=status.HTTP_400_BAD_REQUEST,detail="No records exists")
    
    return query


#Create Request
@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_saving(request:SavingRequest,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    saving = models.Saving(amount=request.amount,user_id=current_user.id)

    db.add(saving)
    db.commit()
    db.refresh(saving)

    return {"detail":{"saving":saving}}


#Update Request
@router.put('/update/{id}',status_code=status.HTTP_200_OK,response_model=SavingResponse,dependencies=[Depends(get_current_user)])
def update_saving(id:int,request:SavingRequest,db:Session=Depends(get_db)):
    saving = db.query(models.Saving).filter(models.Saving.id == id).first()

    if not saving:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No savings exists")
    
    saving.amount = request.amount
    saving.updated_at = datetime.now()

    db.commit()
    db.refresh(saving)

    return saving
