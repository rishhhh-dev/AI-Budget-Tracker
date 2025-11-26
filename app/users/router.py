from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from ..utils.database import *
from ..utils import models
from .auth import *
from .schemas import *
from .token import *

router = APIRouter(
    prefix = '/api/users',
    tags= ['Users & Authentication']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[UserResponse])
def get_users(db:Session=Depends(get_db)):
    query = db.query(models.Users).all()

    if not query:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail='No users found')
    
    return query

@router.post('/register',status_code=status.HTTP_201_CREATED)
def create_user(request:UserRequest,db:Session=Depends(get_db)):
    
    hash_password = Hash.encrypt(request.password)

    user = models.Users(firstname=request.firstname,lastname=request.lastname,email=request.email,password=hash_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {'detail':"User created"}

@router.post('/login',status_code=status.HTTP_200_OK)
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    email = request.username
    password = request.password
    user = db.query(models.Users).filter(models.Users.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Credentials')
    
    if not Hash.verify_password(password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Password')

    get_token = db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user.id).first()


    data = {"id":user.id,"email":user.email}
    print(data,"====Data===")

    if not get_token:
        new_refresh_token = generate_refresh_token(data,db)
        data.update({"refresh_id":new_refresh_token['refresh_id']})
        new_acccess_token = generate_access_token(data,db)
    else:
        data.update({"refresh_id":get_token.id})
        new_acccess_token = generate_access_token(data,db)

    return {"access_token":new_acccess_token['access'],"token_type":"bearer"}
