from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogin
from services.auth import AuthService
from database import get_db

auth_router = APIRouter()

@auth_router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    user = AuthService.register_user(db, user_data)
    token = AuthService.create_access_token(user.id)
    return {"token": token}

@auth_router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = AuthService.create_access_token(user.id)
    return {"token": token}