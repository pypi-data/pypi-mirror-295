# Pydantic models, renamed to 'schemas' to avoid being confused with sqlalchemy models.
from typing import Optional

# from pydantic import BaseModel, Field
from uuid import UUID


class ProjectCreate:
    title: str
    proj_inputs: list
    owner_uuid: Optional[UUID]
    description: Optional[str]
    uuid: Optional[UUID] = None

    class Config:
        orm_mode = True


# Remember to add Config orm_mode=True for classes which are reading db entries
# class Config:
#     orm_mode = True
