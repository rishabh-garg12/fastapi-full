from typing import List, Optional
from unittest import result
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db
from .. import models, oauth
from ..schemas import PostResponce, Post, PostVote

router = APIRouter(
    prefix="/sqlalchemy/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[PostVote])
# this user_id int data type is of no use, it return tokend_Data not int.
def get_posts(db: Session = Depends(get_db), user_id=Depends(oauth.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # .filter(models.Post.owner_id == user_id.id)
    # post = db.query(models.Post).filter(
    # models.Post.title.contains(search)).limit(limit).offset(skip).all()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    print(post)

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponce)
def create_post(post: Post, db: Session = Depends(get_db), user_id: int = Depends(oauth.get_current_user)):
    print(user_id)
    new_post = models.Post(owner_id=user_id.id, **post.dict())
    db.add(new_post)   # To add in db
    db.commit()   # Commit that something added and we are confirm to add in db
    # This is like returning in sql, so it will update our new_post
    db.refresh(new_post)
    # return {"data": new_post}  This is when we didn't define a specific response model
    return new_post


@router.get("/{id}", response_model=PostVote)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return post


@router.delete("/{id}", response_model=PostResponce)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    if post.owner_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"data": post}


@router.put("/{id}", response_model=PostResponce)
def update_post(id: int, post: Post, db: Session = Depends(get_db), user_id: int = Depends(oauth.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    posted = post_query.first()

    if posted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    if posted.owner_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    # post.update({'title': 'Hey this is my updated title',
    #             'content': 'This is my updated content'}, synchronize_session=False)

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
