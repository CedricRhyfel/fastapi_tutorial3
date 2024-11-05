#Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote

"""
models.Base.metadata.create_all(bind=engine)    #Creating/Instanciating all of the models/tables if they don't currently exist when app runs.
04/11/2024: Not needed anymore since use of Alembic (Database Migration Tool)
"""

origins = ["*"]

app = FastAPI() #Creating FastAPI instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello WOrld!"}

    #Including Application's Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
