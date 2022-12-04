
import imp
from fastapi import FastAPI

from . import models
from .database import engine
from .config import settings
from .routers import posts, users, auth, votes
from app import database
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"message": "HelloWorld"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
#  -----xxxxxxxxxxxxxx---------Users Practice-----------xxxxxxxxxxxxx--------- #
