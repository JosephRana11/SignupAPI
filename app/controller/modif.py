from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import User

from keys import local_database_url


database_url = local_database_url

engine = create_engine(database_url)

session_maker = sessionmaker(bind=engine , expire_on_commit=False)



#creates user in the database
def create_new_user(user):
    new_user = User()
    with session_maker() as session:
        session.add(user)
        session.commit()
        return {"Operation" : "Successfull"}


#validates data for user creating . returns None if user data is unique
def confirm_user_is_unique(username , email):
    with session_maker() as session:
        user = session.query(User).filter_by(username = username).first()
        if user is not None:
            return "error"
        user = session.query(User).filter_by(email = email).first()
        if user is not None:
            return "error"
        return None 


#returns user model instance *username
def query_user_data(username):
    with session_maker() as session:
        user = session.query(User).filter_by(username = username).first()
        return user
    

def delete_user(user):
    with session_maker() as session:
        session.delete(user)
        session.commit()
        