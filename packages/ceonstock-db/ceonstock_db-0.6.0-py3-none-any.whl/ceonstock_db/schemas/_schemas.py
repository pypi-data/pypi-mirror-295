# Pydantic models, renamed to 'schemas' to avoid being confused with sqlalchemy models.
from typing import Optional, List, Dict  # Extends data type inputs for fastapi
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from uuid import uuid4, UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    email: str


# Data required to create a user
class UserCreate(UserBase):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


# The user in the DB
class User(UserBase):
    uuid: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    proj_inputs: dict


class JobBase(BaseModel):
    job_id: int


class JobCreate(JobBase):
    user_id: int
    project_id: int


# class Job(JobBase):
