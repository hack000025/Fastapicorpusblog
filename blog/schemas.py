from typing import List, Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    blog_name: str
    comment:str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    username:str
    name:str
    email:str
    password:str


class Get_User_by_id(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode = True



# class Login(BaseModel):
#     username: str
#     password:str
