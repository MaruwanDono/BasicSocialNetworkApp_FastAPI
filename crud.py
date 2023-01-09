from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


#User operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#Post operations
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_user_post(db: Session, post_id: int):
    #db_post = models.Post(**post.dict(), owner_id=user_id)
    post_query = db.query(models.Post).filter_by(id = post_id).all()
    if(post_query and len(post_query)==1):
        #db.query(Post).filter(Post.id == post_id).delete()
        db.delete(post_query[0])
        db.commit()
        #db.refresh(db_post)
        return {"Deleted post": post_query[0]}
    else:
        return {"Unable to delete post with id ": post_id}


def like_user_post(db: Session, post_id: int):
    post_query = db.query(models.Post).filter_by(id = post_id).all()
    #db.query(Post).filter(Post.id == post_id).delete()
    if(post_query and len(post_query) == 1):
        post_query[0].number_of_likes +=1
        db.commit()
        db.refresh(post_query[0])
        return {"Liked post": post_query[0]}
    else:
        return {"Unable to like post with id ": post_id}


def dislike_user_post(db: Session, post_id: int):
    post_query = db.query(models.Post).filter_by(id = post_id).all()
    #db.query(Post).filter(Post.id == post_id).delete()
    if(post_query and len(post_query) == 1):
        post_query[0].number_of_dislikes += 1
        db.commit()
        db.refresh(post_query[0])
        return {"Disliked post": post_query[0]}
    else:
        return {"Unable to dislike post with id ": post_id}
