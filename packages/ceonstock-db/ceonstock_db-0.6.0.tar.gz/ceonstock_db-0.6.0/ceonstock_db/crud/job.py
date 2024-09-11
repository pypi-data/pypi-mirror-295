import logging
from typing import List, Union
from typing import Sequence

from sqlalchemy import select, update, func, and_, desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

# from sqlalchemy.sql import values
from datetime import datetime
from uuid import UUID

from ceonstock_db import models

# from ceonstock_db.models.job_models import (
#     JobTbl,
#     JobProgressTbl,
# )

# from db.engine import SessionLocal

logger = logging.getLogger(__name__)


# def create(db: Session, **values):
def create(
    db: Session,
    user_uuid: UUID,
    project_uuid: UUID,
    submission_uuid: UUID,
    job_type: str,
):
    # Create new job entry
    new_job = models.JobTbl(
        user_account_uuid=user_uuid,
        project_uuid=project_uuid,
        submission_uuid=submission_uuid,
        job_type=job_type,
    )
    db.add(new_job)
    db.flush()
    logger.debug(f"Created new_job: {new_job}")
    # Create new job_progress entry
    new_job_progress = models.JobProgressTbl(job_uuid=new_job.uuid)
    db.add(new_job_progress)
    logger.debug(f"Created new_job_progress: {new_job_progress}")
    db.commit()

    return new_job


def get(db: Session, job_uuid) -> models.JobTbl:
    stmt = select(models.JobTbl).where(models.JobTbl.uuid == job_uuid)
    got_job = db.execute(stmt).scalars().one()
    return got_job


def get_unstarted_jobs(
    db: Session,
) -> Sequence[models.JobProgressTbl]:
    stmt = select(models.JobProgressTbl).where(
        models.JobProgressTbl.assigned_at == None
    )
    got_job = db.execute(stmt).scalars().all()
    return got_job


def get_job_progress(db: Session, job_uuid):
    stmt = select(models.JobProgressTbl).where(
        models.JobProgressTbl.job_uuid == job_uuid
    )
    got_job_progress = db.execute(stmt).scalars().one()
    return got_job_progress


def update_job(db: Session, job_uuid, values_to_set: dict):
    if not values_to_set:
        logger.warning("Received blank values_to_set. Skipping")
        return None
    stmt = (
        update(models.JobTbl)
        .where(models.JobTbl.uuid == job_uuid)
        .values(**values_to_set)
    )
    try:
        # Note: Changes not committed to db until session.flush()/commit() is executed.
        # This logic is handled by the app/API so that DB calls can be minimized
        db.execute(stmt)
        return
    except Exception as e:
        logger.warn(f"Failed to set timestamp in jobqueue: {e}")
        raise Exception(
            f"Failed to update jobqueue timestamps: {values_to_set}"
        )


def update_job_progress(db: Session, job_uuid, values_to_set: dict):
    # job_uuid: The id of the job to update
    # columns_to_timestamp: A list of strings that are the column names
    if not values_to_set:
        logger.warning("Received blank values_to_set. Skipping")
        return None

    # timestamp = datetime.now()
    msgs_to_print = ["Got values_to_set: "]
    for key, value in values_to_set.items():
        msgs_to_print.append(f"\n\t\t{key}: {value}")
    logger.debug("".join(msgs_to_print))
    stmt = (
        update(models.JobProgressTbl)
        .where(models.JobProgressTbl.job_uuid == job_uuid)
        .values(**values_to_set)
    )
    try:
        # Note: Changes not committed to db until session.flush()/commit() is executed.
        # This logic is handled by the app/API so that DB calls can be minimized
        result = db.execute(stmt)
        logger.debug(
            f"Succesfully updated job progress (not committed): {values_to_set}"
        )
        logger.info(f"Got result from db: {result}")
        return values_to_set
    except Exception as e:
        logger.warn(f"Failed to set timestamp in jobqueue: {e}")
        raise Exception(
            f"Failed to update jobqueue timestamps: {values_to_set}"
        )


def get_all(db: Session, page=0, limit=15):
    skip = page * limit
    stmt = (
        select(models.JobTbl)
        .offset(skip)
        .limit(limit)
        .order_by(desc(models.JobTbl.created_at))
    )
    result = db.execute(stmt).scalars().all()
    return result


def get_jobs_by_user_id(db: Session, user_uuid, page=0, limit=15):
    skip = page * limit
    stmt = (
        select(models.JobTbl)
        .where(models.JobTbl.user_account_uuid == user_uuid)
        .offset(skip)
        .limit(limit)
        .order_by(desc(models.JobTbl.created_at))
    )
    result = db.execute(stmt).scalars().all()
    return result


"""
class Job:
    @classmethod
    def get(cls, db: Session, job_uuid):
        stmt = select(models.JobTbl).where(models.JobTbl.uuid == job_uuid)
        got_user = db.execute(stmt).scalars().one()
        return got_user

    @classmethod
    def get_all(cls, db: Session, page=0, limit=15):
        skip = page * limit
        stmt = (
            select(models.JobTbl)
            .offset(skip)
            .limit(limit)
            .order_by(desc(models.JobTbl.uuid))
        )
        result = db.execute(stmt).scalars().all()
        return result

    @classmethod
    def get_jobs_by_user_id(cls, db: Session, user_uuid, page=0, limit=15):
        skip = page * limit
        stmt = (
            select(models.JobTbl)
            .where(models.JobTbl.user_uuid == user_uuid)
            .offset(skip)
            .limit(limit)
            .order_by(desc(models.JobTbl.created_at))
        )
        result = db.execute(stmt).scalars().all()
        return result

    # TODO refactor above func so filtering (see below func) can be an optional argument

    @classmethod
    def get_jobs_by_job_id_list(
        cls, db: Session, user_uuid, job_id_list, page=0, limit=15
    ):
        # returns a user's jobs, filtered by a list of job ids
        skip = page * limit
        stmt = (
            select(models.JobTbl)
            # .where(models.JobTbl.user_uuid == user_uuid)
            .where(
                and_(
                    models.JobTbl.user_uuid == user_uuid,
                    models.JobTbl.uuid.in_(job_id_list),
                )
            )
            .offset(skip)
            .limit(limit)
        )
        result = db.execute(stmt).scalars().all()
        return result

    @classmethod
    def create(cls, db: Session, **values):
        # Create new job entry
        new_job = models.JobTbl(**values)
        db.add(new_job)
        db.flush()
        logger.debug(f"Created new_job: {new_job}")
        # Create new job_progress entry
        new_job_progress = JobProgressTbl(job_uuid=new_job.uuid)
        db.add(new_job_progress)
        logger.debug(f"Created new_job_progress: {new_job_progress}")
        db.commit()

        return new_job


class JobProgress:
    @classmethod
    def get(cls, db: Session, job_uuid):
        stmt = select(JobProgressTbl).where(JobProgressTbl.job_uuid == job_uuid)
        got_job = db.execute(stmt).scalars().one()
        return got_job

    @classmethod
    def get_all(cls, db: Session):
        # TODO only return jobs belonging to user id
        stmt = select(JobProgressTbl).order_by(desc(JobProgressTbl.job_uuid))
        result = db.execute(stmt).scalars().all()
        return result

    @classmethod
    def create(cls, db: Session, **values):
        new_job_progress = JobProgressTbl(**values)
        db.add(new_job_progress)
        db.commit()
        return new_job_progress

    @classmethod
    def set_timestamp(cls, db: Session, job_uuid, columns_to_timestamp):
        # job_uuid: The id of the job to update
        # columns_to_timestamp: A list of strings that are the column names
        if not columns_to_timestamp:
            return None
        if not type(columns_to_timestamp) is list:
            columns_to_timestamp = [columns_to_timestamp]

        timestamp = datetime.now()
        msgs_to_print = ["Got keys to set: "]
        values_to_set = {}
        for key in columns_to_timestamp:
            msgs_to_print.append(f"\n\t\t{key}")
            values_to_set[key] = timestamp
        logger.info("".join(msgs_to_print))
        stmt = (
            JobProgressTbl.update()
            .where(JobProgressTbl.uuid == job_uuid)
            .values(**values_to_set)
        )
        try:
            result = db.execute(stmt).scalars().one()
            logger.info(f"Succesfully set timestamps: {values_to_set}")
            return values_to_set
        except Exception as e:
            logger.warn(f"Failed to set timestamp in jobqueue: {e}")
            raise Exception(f"Failed to update jobqueue timestamps: {values_to_set}")
"""
