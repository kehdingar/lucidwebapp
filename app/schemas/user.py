from pydantic import BaseModel, EmailStr, validator

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_must_be_strong(cls, v):
        # Add password validation logic here
        return v

class UserLogin(UserBase):
    password: str