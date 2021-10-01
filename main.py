from fastapi import FastAPI ,Depends , status , Response , HTTPException
from sqlalchemy.orm import session
from typing import Optional
from starlette import requests
from starlette.routing import Router
from blog import models
from blog import password_hash
from blog.database import engine , SessionLocal
import uvicorn
from blog import models
from blog import schemas
from fastapi import APIRouter
from passlib.context import CryptContext
from blog.password_hash import Hashed_password




app =FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield(db)
    finally:
        db.close()



 

#### UPDATE()#########

@app.put('/CorpusBlog{id}')
def update(id ,request:schemas.BlogBase ,db:session = Depends(get_db)):
    blogs = db.query(models.Blogmodel).filter(models.Blogmodel.id==id)
    if not blogs.first():
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blogs.update({'title': request.title, 'blog_name': request.blog_name , 'comment':request.comment})
    db.commit()
    return 'Resoucre updated successfully'


######CREATE()#########

@app.post('/CorpusBlog' ,status_code=status.HTTP_201_CREATED )
def create(request:schemas.BlogBase , db: session = Depends(get_db)):
    new_blog = models.Blogmodel(title = request.title , blog_name = request.blog_name , comment = request.comment) # nme=reuest.nme
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog 


#########GET()##########

@app.get('/CorpusBlog')
def allblogs(db: session = Depends(get_db)):
    blogs = db.query(models.Blogmodel).all()  
    return blogs



########GET BLOG BY ID ############

@app.get('/CorpusBlog/{id}' ,status_code= 200)
def Blogs_by_id(id,response :Response ,db:session = Depends(get_db)):
    blogs = db.query(models.Blogmodel).filter(models.Blogmodel.id ==id).first() 
    if not blogs:
        raise HTTPException(status.HTTP_404_NOT_FOUND ,msg=f"provided id{id} doesnot exist")   
    return blogs 



##########DELETE BY ID ########

@app.delete('/CorpusBlog/{id}', status_code= status.HTTP_204_NO_CONTENT)
def destroy(id , db:session = Depends(get_db)):
    blog =  db.query(models.Blogmodel).filter(models.Blogmodel.id == id).delete(synchronize_session = False)
    db.commit()
    return 'done'




########## User ##############

@app.post('/corpus/user',status_code=status.HTTP_201_CREATED)
def create(request: schemas.User,db:session = Depends(get_db)):
    user = models.User(username=request.username , name=request.name,email=request.email,password=Hashed_password.bcrypt(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

######### To get User by id ###########

@app.get('/corpus/user{id}', response_model=schemas.Get_User_by_id)
def getuser(id:int,db:session = Depends(get_db)):
    user =db.query(models.User).filter(models.User.id ==id).first() 
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,msg='plz provide valide id user not found with this id {id}') 
    return user
    

















    

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1', port=8000)



