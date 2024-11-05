from fastapi import FastAPI, APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

# Instanciating APIRouter
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# USERS PATH_OPERATIONS:
    #Create a user path-operation.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):    #stores the data received from the body into the variable called "user". Also creating a session called "db" to interact with the database.
    
    hashed_password = utils.hash(user.password)   #Hashing the user's password
    user.password = hashed_password     #Updating the user's password to the new hashed password
        
    new_user = models.User(
        **user.dict() #Convert 'user' variable into an dictionary and unpack it.
    )
    db.add(new_user)    #Add new dictionary to the database.
    db.commit()    #Commit changes
    db.refresh(new_user)    #Return data
    
    return new_user


    #Path-Op to fetch a user's info using its id number
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()   #Stop at the first encounter in the database

    if not user:    #If user with stated id is not found, then
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id: {id} does not exist")    
    return user