import imp
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# SECRET_KEY, for generate our signature
# Algorithm , for generate the jwt
# Expiration time, as the name suggest how much time we want to attempt user a login test


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_min


def create_access_token(data: dict):
    to_encode = data.copy()

    # Providing header info, expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise cred_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise cred_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    # We can directly get our user here by extracting id from verify_acces... method. for this just check video from 7:41:00
    return verify_access_token(token, cred_exception)
