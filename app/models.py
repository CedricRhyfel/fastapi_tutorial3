from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


#THIS IS THE SQLALCHEMY MODEL
#THIS MODEL DEFINES HOW OUR DATABASE, SPECIFIC TABLES, AND OTHERS LOOK LIKE.

#Creating/Initializing the 'posts' table
class Post(Base):
    __tablename__ = "posts"     #Defining the table's name

    id = Column(Integer, primary_key=True, nullable=False)      #Creating the id column
    title = Column(String, nullable=False)      #Title Column 
    content = Column(String, nullable=False)    #Content Column
    published = Column(Boolean, server_default='TRUE', nullable=False)     #Published Column
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")



#Creating users table
class User(Base):
    __tablename__ = 'users'     #Defining the table's name

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String, nullable = True)
    


#Creating votes table
class Vote(Base):
    __tablename__ = "votes"     #Defining the table's name

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)