from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

import psycopg2
from psycopg2.extras import RealDictCursor
import time


#Creating URL to database in a variable
SQLAlchemy_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'
engine = create_engine(SQLAlchemy_DATABASE_URL)    #Creating the engine to establish the connection

# Creating a session to talk to our database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Database Connection [for using raw SQL]
    # while True:
    #     try:
    #         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='pokemon4everxD', 
    #                                 cursor_factory=RealDictCursor)
    #         cursor = conn.cursor()
    #         print("Connection to database successful!")
    #         break
    #     except Exception as error:
    #         print("Connection to database failed :/")
    #         print("Error: ", error)
    #         time.sleep(2)