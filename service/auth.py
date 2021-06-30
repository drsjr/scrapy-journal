from datetime import datetime, timedelta
from database import Database, UserRepository, NewsRepository
from typing import Optional

from model import TokenData, User, UserInDB

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "752b3f39e938f67f65de56f2500f5eadddc1443f04ccaa"
ALGO = "HS256"
ACCESS_TOKE_EXPIRE_MINUTES = 10

repo = UserRepository(Database())

news_repo = NewsRepository(Database())


categories = [ 'ultimas', 'jundiai', 'opiniao', 'politica', 'economia', 'policia', 'esportes', 'cultura', 'hype'] 

pwd_context = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(repo: UserRepository, username: str):
    user = repo.get_query_by_username(username)
    if user is not None: 
        return UserInDB(**dict(user))

def authenticate_user(repo: UserRepository, username: str, password: str):
    user = get_user(repo, username)
    if not user:
        return False

    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKE_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)

    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credential",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(repo, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    return current_user



async def get_new_by_category(category: str, offset: int, limit: int):
    if offset < 0 or limit < 0 or limit > 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="value parameter invalid")

    if category not in categories:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category doesn't exist")

    return news_repo.get_query_category_pagination(category=category, offset=offset,  limit=limit)





