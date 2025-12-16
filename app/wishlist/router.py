from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..users.token import get_current_user
from ..utils.database import get_db
from ..utils import models
from .schemas import *

router = APIRouter(
    prefix= '/api/wishlist',
    tags=['Wishlist']
)


#GET Wishlists
@router.get('/',response_model=List[WishlistResponse],status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def get_wishlists(db:Session=Depends(get_db)):
    
    data = db.query(models.WishList).all()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No Wishlist found')
    
    return data

#Create Wishlist
@router.post('/create',response_model=WishlistResponse,status_code=status.HTTP_201_CREATED)
def create_wishlist(request:WishlistRequest,db:Session=Depends(get_db),current_user=Depends(get_current_user)):

    data = models.WishList(name=request.name,budget=request.budget,goal=request.goal,user_id=current_user.id)

    db.add(data)
    db.commit()
    db.refresh(data)

    return data


#Update Wishlist
@router.put('/update/{id}',response_model=WishlistResponse,status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def update_wishlist(id:int,name:Optional[str],budget:Optional[float],goal:Optional[str],db:Session=Depends(get_db)):

    data = db.query(models.WishList).filter(models.WishList.id == id).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No wishlist found")
    
    if name:
        data.name = name
    
    if budget:
        data.budget = budget
    
    if goal:
        data.goal = goal
    
    db.commit()
    db.refresh(data)

    return data

#Delete wishlist
@router.delete('/delete/{id}',status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def delete_wishlist(id:int,db:Session=Depends(get_db)):
    data = db.query(models.WishList).filter(models.WishList.id == id).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No wishlist found")
    
    db.delete(data)
    db.commit()

    return {"detail":{"income deleted"}}
    
