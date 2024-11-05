from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):  #Storing the data sent by the user into the variable 'user_credentials'. 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()    #Filtering the database to find the user, and storing its db info into 'user'.

    if not user:    # If user is not found
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #if user is found and credentials match:
    #Create Token

    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}