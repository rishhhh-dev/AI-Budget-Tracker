from jose import jwt,JWTError
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime,timedelta
from dotenv import load_dotenv
from ..utils import models
from ..utils.database import *
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_DAYS",30)
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS",7)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

#Generate Refresh Token
def generate_refresh_token(data:dict,db):
    to_encode = data.copy()

    expire = datetime.now()+timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    print(data,"====Data=====")
    token = models.RefreshToken(refresh_token=encode_jwt,user_id=data['id'])
    db.add(token)
    db.commit()
    db.refresh(token)

    return {"refresh":encode_jwt,"refresh_id":token.id}


#Generate ACCESS Token
def generate_access_token(data:dict,db):
    to_encode = data.copy()

    expire = datetime.now()+timedelta(days=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    token = models.AccessToken(access_token=encode_jwt,refresh_id=data['refresh_id'])
    db.add(token)
    db.commit()
    db.refresh(token)


    return {"access":encode_jwt}


#Login Required Funcionality
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("email")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.Users).filter(models.Users.email == user_email).first()
    if user is None:
        raise credentials_exception
    return user