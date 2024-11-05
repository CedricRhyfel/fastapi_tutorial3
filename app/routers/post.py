from fastapi import FastAPI, APIRouter, HTTPException, Depends, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

#Instanciating APIRouter
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# POSTS PATH_OPERATIONS
    #Get all posts
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])   # Specifying that we need a list of the schema.Post model, because the api will send back a list of posts.
def get_posts(db: Session = Depends(get_db),    #Creating a session to interact with the database as a dependency
              current_user:int = Depends(oauth2.get_current_user),    #Verifies a user's token validity
              search: Optional[str] = "",
              limit:int = 20,
              skip:int = 0):

    #SQL procedure of getting all posts:
    # posts = cursor.execute(""" SELECT * FROM posts; """)
    # posts = cursor.fetchall()

#Making a query to the database to retrieve all data from the Post model, and store it in the 'posts' variable.
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)
    # ).limit(limit).offset(skip).all()     

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("upvotes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #NEED TO CHECK!
    # results = list(map(lambda x : x._mapping, results))

    return posts      #Returning the data inside of the 'posts' variable.



    #Create Post Path Operation
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)

# def create_post(payload: dict = Body(...)): #The body of the post request is converted into a python dictionary, which is then stored in the 'payload' variable.

def create_post(post: schemas.PostCreate,   #Holding the body of the posted data as a "Post" pydantic model and storing it in the 'post' variable.
                db: Session = Depends(get_db),  #Instanciating a database session to call CRUD operations on the database.
                current_user: int = Depends(oauth2.get_current_user)):    #Verifies a user's token validity.
    
    #post_dict = post.dict()    #Converting our 'post' variable which currently holds a pydantic model, into a python dictionary
    """
    cursor.execute(INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *, IMPORTANT: there needs to be 3" between the SQL lines!
                   (post.title, post.content)
                   )    #Executing the SQL command
    new_post = cursor.fetchone()    #Fetching the just created post info and storing it in 'new_post' variable.
    conn.commit()   #Commiting the change to the database    

    """

    new_post = models.Post(
        owner_id=current_user.id,   #Adding 'owner_id' in the data returned when creating a new post.
        **post.dict()   #unpacking the fields of the 'Post' table and associating them with the 'post' values given from the front-end.
    )
    db.add(new_post)    #Adding the new_post data into the 'Post' table in the db.
    db.commit()     #Committing the change to the db.
    db.refresh(new_post)    #Returning the data to the front-end.

    return new_post   #returning the new_post data



    #Get One Post Path Operation
@router.get("/{id}", response_model=schemas.PostOut) #FastAPI automatically extracts the path parameter (in this case "id"), which can then be used in our code.
def get_post(id:int,    #Passing the "id" parameter so it can be used in our function.
            db: Session = Depends(get_db),
            current_user:int = Depends(oauth2.get_current_user)):   

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s; """, (str(id)),)        #SQL WAY
    # post = cursor.fetchone()      

    # post = db.query(models.Post).filter(models.Post.id == id).first()   #Filtering all posts' ids in the table and stopping at the 1st_encounter where ids match.

    post = db.query(models.Post, func.count(models.Vote.post_id).label("upvotes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


                                        
    # print(current_user.email)
    if not post:    #If the post is not found.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  #raise this HTTP Exception, with the following details.
                            detail= f"The post with id: {id} does not exist!")
    return post    #If post is found, return it!



    #Delete Post Path-Operation
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,
                db:Session=Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))     #SQL WAY
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)    # Making the query to find the post in the db.
    post = post_query.first()    # Finding the post. Storing the post's data in the variable "post"


    if post == None:    # If the post is not found/doesn't exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Message: Post with id {id} does not exist!")
    
    if post.owner_id != current_user.id:    # If the logged in user is NOT the user that created the post:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # If the logged in user is the one that created the post:
    post_query.delete(synchronize_session=False)    #Making a query to delete from the database.
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



    #Update Post Path-Op
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int,    #Passing the "id" parameter so it can be used in our function.
                updated_post:schemas.PostCreate,    #Holds the body of the posted data in the 'updated_post' variable.
                db:Session=Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):    #Verifies the validity of the user's token

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,   SQL WAY
    #                 (post.title, post.content, post.published, str(id))
    #                 )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)     #Getting the post that needs to be updated
    post = post_query.first()   #Running the query

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Message: Post with id {id} does not exist!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)   #Updating the post with the data as a python dictionary.
    db.commit()     #Committing the change to the database.
    return post_query.first()