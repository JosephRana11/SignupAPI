from fastapi import FastAPI
from pydantic import BaseModel
from models.models import User

from authsys.hash import encrypt_password , check_encrypted_password

from controller.modif import create_new_user , query_user_data , confirm_user_is_unique , delete_user

from fastapi import status , HTTPException 

app = FastAPI()


class base_user(BaseModel):
    username : str
    first_name : str 
    last_name : str 
    email : str 
    password : str 
    confirm_password  : str         

class user_login(BaseModel):
    username : str 
    password : str


class user_delete(BaseModel):
    username : str 
    password : str 
    confirm_password : str

#for root url
@app.get('/')
def root():
    return {"Message" : "Hello world"}


#for creating user
@app.post('/user' , status_code=status.HTTP_201_CREATED)
def get_user(base_user : base_user):
    if base_user.password != base_user.confirm_password:
        raise HTTPException(status_code=404 , detail="Passwords did not match.")
    
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



#for retrieving user information
@app.get('/user/{username}' , status_code=status.HTTP_200_OK)
def get_user(username : str):
    user_data = query_user_data(username)
    print(user_data)
    if user_data is None:
        raise HTTPException(status_code=404 , detail= "User not found")
    else:
        return user_data.dict()

#for deleteing user account
@app.post('/delete-user' , status_code=status.HTTP_200_OK)
def get_user(user_delete : user_delete):
     
    if user_delete.password != user_delete.confirm_password:
        raise HTTPException(status_code=404 , detail="Invalid Credentials")
    
    user = query_user_data(username=user_delete.username)
    
    
    if user is None:
        raise HTTPException(status_code=404 , detail="User Credentials Invalid")
    valid_user = check_encrypted_password(plain_password=user_delete.password , hashed_password=user.hashed_password)

    if valid_user:
        delete_user(user)
        return {"msg" : "Account Deleted Successfully"}
    else:
        raise HTTPException(status_code= 404 , detail="Please enter Correct User password")


#for authenticating user
@app.post('/login' , status_code=status.HTTP_200_OK)
def login_user(login_user : user_login):
    user_data = query_user_data(login_user.username)

    
    #print(user_data.username , user_data.hashed_password)
    validated_user = check_encrypted_password(plain_password=login_user.password , hashed_password=user_data.hashed_password)

    if validated_user == True:
        return {"status" : "User Logged in"}
    else: 
        raise HTTPException(status_code=404 , detail="User Login failed.")


