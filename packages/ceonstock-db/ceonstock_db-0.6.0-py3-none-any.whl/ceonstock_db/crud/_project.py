import logging

from sqlalchemy import select, update, func, and_, desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

# from sqlalchemy.sql import values
from datetime import datetime
from uuid import UUID

from ceonstock_db.models.project_models import ProjectTbl

# from db.engine import SessionLocal

logger = logging.getLogger(__name__)


class Project:
    @classmethod
    def get(cls, db: Session, proj_uuid: UUID, raise_missing=False):
        stmt = select(ProjectTbl).where(ProjectTbl.uuid == proj_uuid)
        try:
            got_project = db.execute(stmt).scalar_one()
        except NoResultFound as e:
            if raise_missing:
                raise e
            return None
        return got_project

    @classmethod
    def get_all(cls, db: Session):
        # TODO only return jobs belonging to user id
        stmt = select(ProjectTbl).order_by(ProjectTbl.title)
        result = db.execute(stmt).scalars().all()
        return result

    @classmethod
    def get_proj_inputs(cls, db: Session, proj_uuid: UUID):
        stmt = select(ProjectTbl.proj_inputs).where(ProjectTbl.uuid == proj_uuid)
        got_project_inputs = db.execute(stmt).one()
        # return got_project["proj_inputs"]
        return got_project_inputs.proj_inputs

    @classmethod
    def create(cls, db: Session, **values):
        """Create a new project row"""
        new_project = ProjectTbl(**values)
        db.add(new_project)
        db.commit()
        return new_project

    @classmethod
    def update(cls, db: Session, proj_uuid: UUID, **values):
        """Update the object or return None if not found."""
        project = db.get(ProjectTbl, proj_uuid)
        if not project:
            logger.info("--NO PROJECT FOUND--")
            return None
        logger.info(f"Got from DB project.uuid({project.uuid}): {project.title}")
        logger.info(f"Got values: {values}")
        # project.update(**values)
        stmt = update(ProjectTbl).where(ProjectTbl.uuid == proj_uuid).values(**values)
        db.execute(stmt)
        # rowcount = result.rowcount
        # logger.info(f"update project result: {result}")
        # logger.info(f"update project rowcount: {rowcount}")
        db.commit()
        return project

    @classmethod
    def upsert(cls, db: Session, proj_uuid: UUID, **values):
        """Update the object or create a new entry if not found."""
        new_project = ProjectTbl(uuid=proj_uuid, **values)
        db.merge(new_project)
        db.commit()

    @classmethod
    def delete(cls, db: Session, proj_uuid: UUID):
        project = db.get(ProjectTbl, proj_uuid)
        logger.info(f"Got project for deletion: {project}")
        db.delete(project)
        db.commit()
        logger.info(f"Deleted proj({proj_uuid}) from db.")
        return proj_uuid
