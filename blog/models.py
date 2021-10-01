from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
# from sqlalchemy.orm import relationship
from pydantic import BaseModel

class Blogmodel(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    blog_name = Column(String)
    comment = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    # name_of_user = relationship("User", back_populates="created_blogs")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    # created_blogs = relationship('Blog', back_populates="name_of_user")

class GetUser(BaseModel):
    username:str
    email:str
    email:str
    # blogs : List[Blog] =[]
    class Config():
        orm_mode = True