# Pydantic models, renamed to 'schemas' to avoid being confused with sqlalchemy models.
from uuid import UUID
from typing import Optional  # Extends data type inputs for fastapi

# from pydantic import BaseModel, Field, EmailStr


class JobBase:
    job_uuid: UUID


class JobCreate(JobBase):
    user_uuid: UUID
    project_uuid: UUID


# class Job(JobBase):

# class Config:
#     orm_mode = True
