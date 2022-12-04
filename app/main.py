from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

from sqlalchemy.orm import Session
from . import models
from .schemas import Post
from .database import engine, get_db


# This is for practice without python to db(sqlAlchemy orm)

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
# This is making connetion or session with the db which is responsible for communicate all path operations to db


try:
    conn = psycopg2.connect(
        host='localhost', database='fastapi', user='postgres', password='Rishi@123', cursor_factory=RealDictCursor)

    cursor = conn.cursor()
    print("Database connection was successfull!")
except Exception as error:
    print("Connection to database failed")
    print("Error: ", error)

my_posts = [
    {
        "title": "Hello rishabh",
        "content": "check out",
        "rating": "4",
        "id": 1,
    },
    {
        "title": "Hello rishu",
        "content": "check this out",
        "rating": "5",
        "id": 2
    }
]


def find_post(id):
    for i in my_posts:
        if (i["id"] == id):  # int(id) to convert to int
            return i


def find_index(id):
    for i, p in enumerate(my_posts):
        if (p["id"] == id):
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     return {"status": "success"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# also /createposts but that doesn't follow best practices, ("/posts", status_code = status.HTTP_201_CREATED) because docs say 201 for creating


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(body: dict = Body(...)):
def create_post(post: Post):       # This is when we use pydantic models
    print(post.dict())  # post.title for single property
    post_here = post.dict()
    post_here["id"] = randrange(1, 10000000)
    my_posts.append(post_here)
    return {"Data": post_here}


@app.get("/posts/{id}")
# int is neccessary so as to validate that from frontend we get an integer number nor string
# for response below import from fast api and pass in with the path (id: int, response: Response):
def get_post(id: int):
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"Data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete post
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't not exist")
    my_posts.remove(post)
    # return {"Data": post, "Deleted": True}  # we can't return anything in 204
    # or return Response(status.HTTP_204....)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)
    print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

# DB requests


@app.get("/db/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    post = cursor.fetchall()
    return {"data": post}


@app.post("/db/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts(title, content, published) VALUES
    (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"Data": new_post}


@app.get("/db/posts/{id}")
def get_posts(id: int):
    cursor.execute(" SELECT * FROM posts WHERE id = %s ", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    return {"data": post}


@app.delete("/db/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/db/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, id))

    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't not exist")

    return {"data": post}
