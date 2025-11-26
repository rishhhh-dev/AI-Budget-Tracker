from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .schemas import *
from ..utils import models
from ..utils.database import get_db
from ..users.token import get_current_user

router = APIRouter(
    prefix = '/api/category',
    tags = ['Category']
)

#Get Categories
@router.get('/list',response_model=List[CategoryRespone],status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def get_categories(db:Session=Depends(get_db)):
    categories = db.query(models.Category).all()

    if not categories:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'No categories exists')

    return categories

#Get Single Category
@router.get('/list/{name}',response_model=CategoryRespone,status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def get_categories(name:str,db:Session=Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.name == name).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'No with this {name} exists')

    return category


#Create Category
@router.post('/create',status_code=status.HTTP_201_CREATED,dependencies=[Depends(get_current_user)])
def create_category(request:CategoryRequest,db:Session=Depends(get_db)):
    data = db.query(models.Category).filter(models.Category.name==request.name).first()

    if data:
        return {"detail":"This category already exists"} 
    else:
        data = models.Category(name=request.name)
        db.add(data)
        db.commit()
        db.refresh(data)

        return {"detail":{"category":data}}

#Update Category
@router.put('/update/{name}',response_model=CategoryRespone,status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def update_category(request:CategoryRequest,db:Session=Depends(get_db)):
    data = db.query(models.Category).filter(models.Category.name==request.name).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid name")

    data.name = request.name
    data.updated_at = datetime.now()

    return data

#Delete Category
@router.delete('/delete/{name}',status_code=status.HTTP_200_OK,dependencies=[Depends(get_current_user)])
def delete_category(request:CategoryRequest,db:Session=Depends(get_db)):
    data = db.query(models.Category).filter(models.Category.name==request.name).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid name")
    
    db.delete(data)
    db.commit()

    return {"detail":"Category deleted"}