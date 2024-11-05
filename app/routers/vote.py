from fastapi import FastAPI, APIRouter, HTTPException, Depends, Response, status
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session


#Instanciating APIRouter
router = APIRouter(
    prefix="/vote",     #Setting a prefix to every path-operation.
    tags=['Votes']      #Setting the section for the documentation.
)


# Voting Path-Operations

@router.post("/", status_code=status.HTTP_201_CREATED)    #Path-op for voting a post
def vote(vote:schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):     #Getting the current_user's data.
    
    #Logic to check if the post exists:
    post = db.query(models.Post).filter(models.Post.id == vote.post_id)    #Query to check if the post with specified id exists.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{vote.post_id} does not exist!")


    #check if vote exists and if vote_user_id == current_user
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)     #Is the vote's user_id the same as the current user logged in?
    found_vote = vote_query.first()    #Finding the vote in the db

    if (vote.dir == True):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on the post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exists...")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote deleted"}


"""
def vote(vote:schemas.Vote,     #Storing the posted data in the variable 'vote', using the 'Vote' schema.
            db: Session = Depends(database.get_db),     #Creating a session to interact with the database.
            current_user: int = Depends(oauth2.get_current_user)):     #Getting the current_user's data.
    
    #check if vote exists and if vote_user_id == current_user
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,    #Does the post_id the same as the post_id in our db table?
        vote.user_id == current_user.id)     #Is the vote's user_id the same as the current user logged in?
    found_vote = vote_query.first()    #Finding the vote in the db
"""