from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, utils, oauth
from ..database import get_db
from ..schemas import UserLogin, Token


router = APIRouter(tags=['Authentication'])

# Remember that in path we provide a pydantic model, and in querying db we do in same data table in which data is stored

# Instead of taking user login info in body we take it in form data, that's why fastapi OAuth2PasswordRequestForm dependency


@router.post('/login', response_model=Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # When we take in form data that it refer only two field, 1. username 2. password.  so in quering we have to check our email with username

    user = db.query(models.User).filter(
        models.User.email == user_cred.username).first()

    # This will check that user exist or not, mainly the email check
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials ")

    # If they provided wrong pass
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # If all goes right, then create our token and return it
    access_token = oauth.create_access_token(
        data={"user_id": user.id})  # Payload data

    return {"access_token": access_token, "token_type": "bearer"}
