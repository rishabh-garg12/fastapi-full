
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from pydantic.types import conint

from app import database
from .models import User


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponce(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


class PostResponce(Post):
    created_at: datetime
    owner_id: int
    id: int
    owner: UserResponce

    class Config:
        orm_mode = True


class PostVote(BaseModel):
    Post: PostResponce
    votes: int

    # class Config:   # not neccessary here as it only return PostResponce
    #     orm_mode = True

#  -----xxxxxxxxxxxxxx---------Users Practice-----------xxxxxxxxxxxxx--------- #


class Token(BaseModel):
    access_token: str
    token_type: str

# for providing our payload data to verify jwt


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
