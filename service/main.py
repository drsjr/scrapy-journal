
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from auth import Token, User

import auth
import json

app = FastAPI()


list_news = json.loads(open("list_news.json", "r").read())
list_articles = json.loads(open("list_article.json", "r").read())


@app.get("/news/{news_id}")
def article(news_id: int):
    return get_article_by_id(news_id)


@app.get("/news")
def news():
    return get_list_news()

def get_list_news():
    return list_news

def get_article_by_id(id: int):
    return list_articles[id]



#####################################
#   Authentication Section          #
#####################################

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(auth.fake_user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKE_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(auth.get_current_active_user)):
    return [{"item_id": "Too", "owner": current_user.full_name}]



