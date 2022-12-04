from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(passw: str):
    return pwd_context.hash(passw)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
