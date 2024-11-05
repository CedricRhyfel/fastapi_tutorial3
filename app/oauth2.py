from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET KEY
#ALGORITHM
#EXPIRATION DATE


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


#Function to create a JWT Token with a dictionary as input
def create_access_token(data: dict):
    to_encode = data.copy()    #Creating a copy of the data provided to manipulate it, while keeping the original data intact.

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    #Creating the expiration time of the token, and storing it in the 'expire' variable.
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)    #Generating a JWT Token and storing it.

    return encoded_jwt    #Returning the token


#Function to verify a JWT Token
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])   #Decoding the JWT Token gives back the payload info.
        id: str = payload.get("user_id")    #Storing the user_id data from the payload into the variable 'id'

        if id is None:    # If id is not found,
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))    #Validating the TokenData with a schema, which is currently just an id
    except JWTError:
        raise credentials_exception
    return token_data


#Function to get the current user's id
def get_current_user(token: str = Depends(oauth2_scheme),
                     db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={
        "WWW-Authenticate": "Bearer"
    })

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user