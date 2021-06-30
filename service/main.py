
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from model import Token, User

import auth
import json

app = FastAPI()



#####################################
#   Authentication Section          #
#####################################

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(auth.repo, form_data.username, form_data.password)
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

@app.get("/news/{category}")
async def news(category: str = 'ultimas', offset: int = 0, limit: int = 5, current_user: User = Depends(auth.get_current_active_user)):
    return await auth.get_new_by_category(category=category, offset=offset, limit=limit)



