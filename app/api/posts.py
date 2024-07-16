from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.post import PostCreate, PostResponse
from services.post import PostService
from services.auth import get_current_user
from database import get_db

posts_router = APIRouter()

@posts_router.post("/")
def create_post(post_data: PostCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    post = PostService.create_post(db, post_data, user.id)
    return PostResponse.from_orm(post)

@posts_router.get("/")
def get_posts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    posts = PostService.get_user_posts(db, user.id)
    return [PostResponse.from_orm(post) for post in posts]

@posts_router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    post = PostService.get_post(db, post_id)
    if not post or post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    PostService.delete_post(db, post)
    return {"message": "Post deleted successfully"}