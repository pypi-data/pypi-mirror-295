import logging
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from ceonstock_db.models.submission import SubmissionTbl
from typing import Optional

logger = logging.getLogger(__name__)


def create(
    db,
    user_uuid: str,
    project_uuid: str,
    submission_uuid: Optional[str],
):
    logger.info(
        f"Received values: {submission_uuid=}, {user_uuid=}, {project_uuid=}"
    )
    new_submission = SubmissionTbl(
        user_account_uuid=user_uuid,
        project_uuid=project_uuid,
        uuid=submission_uuid,
    )
    db.add(new_submission)
    db.commit()
    return new_submission


def get(db: Session, submission_uuid: UUID):
    # TODO switch to ORM workflow (is select ORM?)
    stmt = select(SubmissionTbl).where(SubmissionTbl.uuid == submission_uuid)
    got_submission = db.execute(stmt).scalars().one()
    return got_submission


# def get_by_job_uuid(db: Session, job_uuid: UUID) -> SubmissionTbl:
#     stmt = select(SubmissionTbl).where(SubmissionTbl.job_uuid == job_uuid)
#     got_submission = db.execute(stmt).scalars().one()
#     return got_submission
