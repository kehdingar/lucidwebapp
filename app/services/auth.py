from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User
from schemas.user import UserCreate
from passlib.hash import bcrypt
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate):
        user = User(email=user_data.email, hashed_password=bcrypt.hash(user_data.password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not bcrypt.verify(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(user_id: int):
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode = {"exp": expire, "sub": str(user_id)}
        encoded_jwt = jwt.encode(to_encode, "secret_key", algorithm="HS256")
        return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user