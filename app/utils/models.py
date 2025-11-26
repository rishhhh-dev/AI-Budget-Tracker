from sqlalchemy import Column,Integer,ForeignKey,String,Float,DateTime,Date,Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime
from .database import Base


#Goal Choices
class Goal(str,Enum):
    long_term = 'long'
    short_term = 'short'


#User Table
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    firstname = Column(String(100),nullable=True)
    lastname = Column(String(100),nullable=True)
    email = Column(String(200),nullable=False,unique=True)
    password = Column(String(100),nullable=False,unique=True)
    created_at = Column(DateTime,default=datetime.now())
    token = relationship("RefreshToken",back_populates='user')
    expense = relationship("Expense",back_populates='user')
    income = relationship("Income",back_populates='user')
    saving = relationship("Saving",back_populates='user')
    wishlist = relationship("WishList",back_populates='user')
    budget = relationship("BudgetRule",back_populates='user')


#Refresh Token Table
class RefreshToken(Base):
    __tablename__ = 'refreshtoken'

    id = Column(Integer,primary_key=True,index=True)
    refresh_token = Column(String,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"))
    created_at = Column(DateTime,default=datetime.now())

    user = relationship("Users",back_populates="token")
    access = relationship("AccessToken",back_populates="refresh")


#Access Token Table
class AccessToken(Base):
    __tablename__ = 'accesstoken'

    id = Column(Integer,primary_key=True,index=True)
    access_token = Column(String,nullable=False)
    refresh_id = Column(Integer,ForeignKey('refreshtoken.id'))
    created_at = Column(DateTime,default=datetime.now())

    refresh = relationship("RefreshToken",back_populates="access")


#Expense Table
class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(250),nullable=False)
    amount = Column(Float,nullable=False,default=0.0)
    remark = Column(String,nullable=True,default='')
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())

    user_id = Column(Integer,ForeignKey('users.id'))
    category_id = Column(Integer,ForeignKey('category.id'))

    user = relationship("Users",back_populates="expense")
    category = relationship("Category",back_populates="expense")


#Income Table
class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer,primary_key=True,index=True)
    classify = Column(String(250),nullable=False)
    amount = Column(Float,nullable=False,default=0.0)
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())

    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship("Users",back_populates="income")

#Saving Table
class Saving(Base):
    __tablename__ = 'savings'

    id = Column(Integer,primary_key=True,index=True)
    amount = Column(Float,nullable=False,default=0.0)
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())

    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship("Users",back_populates="saving")

#Wishlist Table
class WishList(Base):
    __tablename__ = 'wishlists'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(250),nullable=False)
    budget = Column(Float,nullable=False,default=0.0)
    goal = Column(SqlEnum(Goal),nullable=False)
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())

    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship("Users",back_populates="wishlist")


#Category Table
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(250),nullable=False,unique=True)

    expense = relationship("Expense",back_populates='category')
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())


#BudgetRule Table
class BudgetRule(Base):
    __tablename__ = 'budgetrule'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(250),nullable=False,unique=True)

    needs_percent = Column(Integer,nullable=False)
    wants_percent = Column(Integer,nullable=False)
    saving_percent = Column(Integer,nullable=False)
    created_at = Column(DateTime,default=datetime.now())

    user_id = Column(Integer,ForeignKey("users.id"))

    user = relationship("Users",back_populates="budget")