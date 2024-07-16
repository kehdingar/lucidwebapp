from sqlalchemy.orm import Session
from models.post import Post
from schemas.post import PostCreate
from api.utils import cache

class PostService:
    @staticmethod
    def create_post(db: Session, post_data: PostCreate, user_id: int):
        post = Post(text=post_data.text, user_id=user_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def get_user_posts(db: Session, user_id: int):
        @cache(ttl=300)
        def get_posts(user_id):
            return db.query(Post).filter(Post.user_id == user_id).all()
        return get_posts(user_id)

    @staticmethod
    def get_post(db: Session, post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def delete_post(db: Session, post: Post):
        db.delete(post)
        db.commit()