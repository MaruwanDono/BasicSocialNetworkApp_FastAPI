from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
import random
from datetime import datetime


def idGenerator(label):
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    random_key = ''.join(random.choice(letters) for i in range(5))
    current_timestamp = datetime.now().timestamp()
    current_timestamp = str(current_timestamp).replace('.','')
    id = "{}-{}-{}".format(label, random_key, current_timestamp)
    return id


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    #number_of_posts = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    number_of_likes = Column(Integer, default=0)
    number_of_dislikes = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
