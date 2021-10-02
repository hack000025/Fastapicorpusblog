from fastapi import FastAPI ,Depends , status , Response , HTTPException
from sqlalchemy.orm import session
from typing import Optional
from starlette import requests
from starlette.routing import Router
from blog import models
from blog import password_hash
from blog import database
from blog.database import engine , SessionLocal
import uvicorn
from blog import models
from blog import schemas
from fastapi import APIRouter
from passlib.context import CryptContext
from blog.password_hash import Hashed_password
from blog import jwt_token
from blog import oauth2


app =FastAPI()


models.Base.metadata.create_all(engine)




get_db = database.get_db






###############login#############

@app.post('/login' ,tags=['authentication'])
def login(request:schemas.Login ,db:session = Depends(get_db)):
    qinst = session.query(models.User).filter_by(models.User.email ==request.username)
   
    if not qinst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,msg=f"user not found")
    if not Hashed_password.verify(request.password ,qinst.password ):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,msg=f"plz enter correct password")

    access_token = jwt_token.create_access_token(data={"sub": qinst.email})
    return {"access_token": access_token, "token_type": "bearer"}






 

#### UPDATE()#########

@app.put('/CorpusBlog{id}',tags=['corpusvision_blogs'])
def update(id ,request:schemas.BlogBase ,db:session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blogmodel).filter(models.Blogmodel.id==id)
    if not blogs.first():
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blogs.update({'title': request.title, 'blog_name': request.blog_name , 'comment':request.comment})
    db.commit()
    return 'Resoucre updated successfully'


######CREATE()#########

@app.post('/CorpusBlog' ,status_code=status.HTTP_201_CREATED ,tags=['corpusvision_blogs'])
def create(request:schemas.BlogBase , db: session = Depends(get_db)):
    new_blog = models.Blogmodel(title = request.title , blog_name = request.blog_name , comment = request.comment) # nme=reuest.nme
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog 


#########GET()##########

@app.get('/CorpusBlog',tags=['corpusvision_blogs'])
def allblogs(db: session = Depends(get_db)):
    blogs = db.query(models.Blogmodel).all()  
    return blogs



########GET BLOG BY ID ############

@app.get('/CorpusBlog/{id}' ,status_code= 200,tags=['corpusvision_blogs'])
def Blogs_by_id(id,response :Response ,db:session = Depends(get_db)):
    blogs = db.query(models.Blogmodel).filter(models.Blogmodel.id ==id).first() 
    if not blogs:
        raise HTTPException(status.HTTP_404_NOT_FOUND ,msg=f"provided id{id} doesnot exist")   
    return blogs 



##########DELETE BY ID ########

@app.delete('/CorpusBlog/{id}', status_code= status.HTTP_204_NO_CONTENT ,tags=['corpusvision_blogs'])
def destroy(id , db:session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog =  db.query(models.Blogmodel).filter(models.Blogmodel.id == id).delete(synchronize_session = False)
    db.commit()
    return 'done'




########## User ##############

@app.post('/corpus/user',status_code=status.HTTP_201_CREATED ,tags=['user'])
def create(request: schemas.User,db:session = Depends(get_db)):
    user = models.User(username=request.username , name=request.name,email=request.email,password=Hashed_password.bcrypt(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

######### To get User by id ###########

@app.get('/corpus/user{id}', response_model=schemas.Get_User_by_id,tags=['user'])
def getuser(id:int,db:session = Depends(get_db)):
    user =db.query(models.User).filter(models.User.id ==id).first() 
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,msg='plz provide valide id user not found with this id {id}') 
    return user
    


















    

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1', port=8000)



