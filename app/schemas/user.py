from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    created_at: datetime


class ProfileBase(BaseModel):
    name: str

class ProfileCreate(ProfileBase):
    pass

class ProfileRead(ProfileBase):
    id: int



class UserWithProfileRead(UserRead):
    profile: ProfileRead