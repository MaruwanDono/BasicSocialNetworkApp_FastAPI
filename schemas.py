from pydantic import BaseModel


#Interaction model
class Interaction(BaseModel):
    id: int
    user_id: int
    post_interaction: bool
    post_id: int

    class Config:
        orm_mode = True


#Post model
class PostBase(BaseModel):
    content: str | None = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    number_of_likes: int
    number_of_dislikes: int
    owner_id: int
    interactions: list[Interaction] = []

    class Config:
        orm_mode = True


#Token model
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


#User model
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    posts: list[Post] = []

    class Config:
        orm_mode = True
