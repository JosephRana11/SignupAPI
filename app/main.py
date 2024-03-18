from fastapi import FastAPI
from pydantic import BaseModel
from models.models import User

from authsys.hash import encrypt_password

from controller.modif import create_new_user , query_user_data , confirm_user_is_unique

app = FastAPI()


class base_user(BaseModel):
    username : str
    first_name : str 
    last_name : str 
    email : str 
    password : str 
    confirm_password  : str         


#for root url
@app.get('/')
def root():
    return {"Message" : "Hello world"}


#for creating user
@app.post('/user')
def get_user(base_user : base_user):
    if base_user.password != base_user.confirm_password:
        return {"Error" : "Passwords don't match"}
    
    #Checking for duplicate user
    duplicate_user = confirm_user_is_unique(email=base_user.email , username=base_user.username)

    if duplicate_user is not None:
        return duplicate_user

    #populating user model with data
    new_password = encrypt_password(base_user.password)
    print(new_password)
    user = User(username = base_user.username , 
                first_name = base_user.first_name ,
                  last_name = base_user.last_name 
                , email = base_user.email , hashed_password = new_password)   
    print(user.dict())
    
    create_new_user(user)

    return {"msg":"User Created Succesfully"}




@app.get('/user/{username}')
def get_user(username : str):
    user = query_user_data(username)
    return user

