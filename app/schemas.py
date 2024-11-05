from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

#THIS IS THE PYDANTIC MODEL

#Creating PyDantic Model to validate posting data to the API.
#IMPORTANT: ALL OF OUR PYDANTIC MODELS HAVE TO EXTEND 'BaseModel'

class PostBase(BaseModel):
    title: str  # The variable 'title' should be a string. If not, the API will send an error.
    content: str
    published: bool = True  #variable will be true by default, if it is not specified.



class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class Post(PostBase):   #Schema for sending out a post
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True      #since we're using pydantic V2, from attributes = orm_mode


class PostOut(BaseModel):    #Schema for retrieving posts with votes.
    Post: Post
    upvotes: int
    class Config:
        from_attributes = True      #since we're using pydantic V2, from attributes = orm_mode



# class PostOut(BaseModel):
#     title: str  # The variable 'title' should be a string. If not, the API will send an error.
#     content: str
#     published: bool = True  #variable will be true by default, if it is not specified.
#     id: int
#     created_at: datetime
#     owner_id: int
#     owner: UserOut
#     votes: int
#     class Config:
#         from_attributes = True      #since we're using pydantic V2, from attributes = orm_mode    votes: int





class UserCreate(BaseModel):
    email: EmailStr
    password: str





class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


#Votes Schemas
class Vote(BaseModel):
    post_id: int
    dir: bool
