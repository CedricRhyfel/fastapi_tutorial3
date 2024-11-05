from passlib.context import CryptContext    #CryptContext is used to hash password


#Hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   #Creating an instance of CryptContext, using the 'bcrypt' algorithm, to hash users' passwords.
def hash(password: str):
    return pwd_context.hash(password)

#Verifying if a given password is the same as the hashed password stored in the db.
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)