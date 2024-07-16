from pydantic import BaseModel, validator
from typing import Optional

class PostBase(BaseModel):
    text: str

    @validator('text')
    def text_must_not_exceed_1mb(cls, v):
        if len(v.encode('utf-8')) > 1024 * 1024:
            raise ValueError('Post text must not exceed 1 MB')
        return v

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True