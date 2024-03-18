from sqlalchemy.orm import declarative_base 
from sqlalchemy import Column , String , DateTime , Integer 
import uuid
from datetime import datetime
from sqlalchemy_utils import EmailType

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "user"

    id = Column(String , primary_key= True , default=generate_uuid)
    created = Column(DateTime , nullable=False , default=datetime.now)
    username = Column(String , nullable=False)
    first_name = Column(String , nullable= False)
    last_name = Column(String , nullable=False)
    email = Column(EmailType , nullable=False)
    hashed_password = Column(String , nullable=False)

    def dict(self):
        return {
            "id" : self.id , 
            "created" : self.created , 
            "username" : self.username,
            "first_name" : self.first_name , 
            "last_name" : self.last_name , 
            "email" : self.email,
        }