# Pydantic models, renamed to 'schemas' to avoid being confused with sqlalchemy models.
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class UserProfileCreate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None


# Data required to create a new user
class UserAccountCreate(BaseModel):
    email: str
    password: str
    profile: Optional[UserProfileCreate] = None


# WIP move all non-create schemas to the API/external applications
# Only handle DB creation schemas/data in this package

# class UserAccountOut(UserAccountBase):
#   profile: Optional[UserProfileOut]

# ORM mode for the class that mirrors the DB
# class Config:
#   orm_mode = True
