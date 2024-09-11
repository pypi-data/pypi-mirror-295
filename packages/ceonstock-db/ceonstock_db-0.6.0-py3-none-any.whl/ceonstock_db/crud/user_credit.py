# For handling user tokens for free project renders, free previews etc.
# Also acts as a way to give a user a free purchase of a project.
import logging
from datetime import datetime, timezone, timedelta
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import exc
from sqlalchemy import select
from sqlalchemy import and_

from ceonstock_db import models
from ceonstock_db import schemas
from ceonstock_db.auth import security
from ceonstock_db import errors

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")


# def get_by_email(db: Session, email: str) -> user_models.UserAccountTbl:
#     stmt = select(user_models.UserAccountTbl).where(
#         user_models.UserAccountTbl.email == email
#     )
#     try:
#         got_user = db.execute(stmt).scalars().one()
#     except exc.NoResultFound:
#         raise errors.NotFoundInDBError(f"Could not find user by email: {email}")
#     logger.debug(f"Returning: {got_user}")
#     return got_user


# def get_all(db: Session):
#     stmt = select(models.user_credit.ReusablePreviewTokenTbl).order_by(
#         models.user_credit.ReusablePreviewTokenTbl.created_at
#     )
#     result = db.execute(stmt).scalars().all()
#     logger.debug(f"result: {result}")
#     return result


# TODO get by comparing available date
# def get_available_reusable_credits_for_user(db: Session, user_uuid: UUID):
#     stmt = select(models.user_credit.ReusablePreviewTokenTbl).where(
#         models.user_credit.ReusablePreviewTokenTbl.user_account_uuid == user_uuid
#     )
#     try:
#         credits_in_db = db.execute(stmt).scalars().all()
#     except exc.NoResultFound:
#         raise errors.NotFoundInDBError(
#             f"Could not find credits for user uuid: {user_uuid}"
#         )
#     logger.debug(f"Returning: {credits_in_db}")
#     return credits_in_db


def get_reusable_credits_for_user(db: Session, user_uuid: UUID):
    stmt = select(models.user_credit.ReusablePreviewTokenTbl).where(
        models.user_credit.ReusablePreviewTokenTbl.user_account_uuid
        == user_uuid
    )
    try:
        credits_in_db = db.execute(stmt).scalars().all()
    except exc.NoResultFound:
        raise errors.NotFoundInDBError(
            f"Could not find credits for user uuid: {user_uuid}"
        )
    logger.debug(f"Returning: {credits_in_db}")
    return credits_in_db


# def redeem_reusable_preview_credit(db: Session, reusable_preview_credit_uuid: UUID):
#     def is_available(preview_credit_in_db):
#         return preview_credit_in_db.available_at <= datetime.now(timezone.utc)

#     def calculate_next_available_time(wait_time_days: float = 30):
#         return datetime.now(timezone.utc) + timedelta(days=wait_time_days)

#     stmt = select(models.user_credit.ReusablePreviewTokenTbl).where(
#         models.user_credit.ReusablePreviewTokenTbl.uuid == reusable_preview_credit_uuid
#     )

#     try:
#         reusable_preview_credit_in_db = db.execute(stmt).scalar_one()
#     except exc.NoResultFound:
#         raise errors.NotFoundInDBError(
#             f"Could not find reusable preview credit with uuid: {reusable_preview_credit_uuid}"
#         )
#     logger.info(f"Got reusable credit for redemption: {reusable_preview_credit_in_db}")
#     available_at = reusable_preview_credit_in_db.available_at
#     logger.info(f"Available at: {available_at}")
#     if not is_available(reusable_preview_credit_in_db):
#         raise Exception(
#             "Tried to redeem an unavailable render credit TODO proper exception handling"
#         )
#     next_available_time = calculate_next_available_time()
#     logger.info(f"Setting new available_at: {next_available_time}")
#     reusable_preview_credit_in_db.available_at = next_available_time
#     logger.warning("Commiting change to db...")
#     db.commit()

#     logger.warning(f"Returning: {reusable_preview_credit_in_db}")
#     return reusable_preview_credit_in_db


def redeem_reusable_preview_credit_for_user(db: Session, user_uuid: UUID):
    # Get the first available reusable preview credit and redeem it (update the 'available at' to a future date)
    def is_available(preview_credit_in_db):
        return preview_credit_in_db.available_at <= datetime.now(timezone.utc)

    def calculate_next_available_time(wait_time_days: float = 30):
        return datetime.now(timezone.utc) + timedelta(days=wait_time_days)

    stmt = select(models.user_credit.ReusablePreviewTokenTbl).where(
        models.user_credit.ReusablePreviewTokenTbl.user_account_uuid
        == user_uuid,
        models.user_credit.ReusablePreviewTokenTbl.available_at
        <= datetime.now(timezone.utc),
    )

    try:
        reusable_preview_credit_in_db = db.scalars(stmt).first()
        if not reusable_preview_credit_in_db:
            raise errors.NotFoundInDBError(
                f"Could not find available preview credit for user with uuid: {user_uuid}"
            )
    except exc.NoResultFound:
        raise errors.NotFoundInDBError(
            f"Could not find available preview credit for user with uuid: {user_uuid}"
        )
    logger.info(
        f"Got reusable credit for redemption: {reusable_preview_credit_in_db}"
    )
    available_at = reusable_preview_credit_in_db.available_at
    logger.info(f"Available at: {available_at}")
    if not is_available(reusable_preview_credit_in_db):
        raise Exception(
            "Tried to redeem an unavailable render credit TODO proper exception handling"
        )
    next_available_time = calculate_next_available_time()
    logger.info(f"Setting new available_at: {next_available_time}")
    reusable_preview_credit_in_db.available_at = next_available_time
    logger.warning("Commiting change to db...")
    db.commit()
    logger.warning("Committed.")

    logger.warning(f"Returning: {reusable_preview_credit_in_db}")
    return reusable_preview_credit_in_db


def create_reusable_preview_credit(db: Session, user_account_uuid: UUID):
    logger.debug(f"Creating new credit for user uuid: {user_account_uuid}")
    new_credit = models.user_credit.ReusablePreviewTokenTbl(
        user_account_uuid=user_account_uuid
    )
    logger.debug(f"Adding new token: {new_credit}")
    db.add(new_credit)
    logger.debug(f"Added new credit to session: {new_credit}")

    logger.debug(f"Flushing new credit to session: {new_credit}")
    try:
        db.flush()
    except exc.SQLAlchemyError as e:
        msg = f"Failed to create new credit for user uuid: {user_account_uuid}"
        errors.handle_sql_error(e, msg=msg)
    logger.debug(f"Flushed new credit to session: {new_credit}")

    # -- Commit Changes --
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        msg = f"Failed to commit changes for new credit for user_uuid: {user_account_uuid}"
        errors.handle_sql_error(e, msg=msg)
    logger.info(f"Committed new credit to db: {new_credit.uuid}")

    return new_credit
