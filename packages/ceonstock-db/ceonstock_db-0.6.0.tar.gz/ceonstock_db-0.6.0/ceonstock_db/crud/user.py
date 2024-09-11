# Test
import logging
import time
from enum import Enum
from typing_extensions import Literal
from typing import get_args
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import exc
from sqlalchemy import select

from ceonstock_db.models import user as user_models

# from ceonstock_db.auth import security
from ceonstock_db import errors
from .oauth_account import OAuthProvider, OAuthProviderValue

# TODO can proj_crud safely auto-fetch the SessionLocal without it needing to be passed?
# from db.engine import SessionLocal

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")


# Currently not being used since api almost always starts interaction with an email get
# Leaving here in case it needs to be reactivated
# def get(db: Session, user_uuid: UUID) -> user_models.UserTbl:
#     logger.debug(f"Getting user by id: {user_uuid}")
#     stmt = select(user_models.UserTbl).where(
#         user_models.UserTbl.uuid == user_uuid
#     )
#     try:
#         got_user = db.execute(stmt).scalars().one()
#     except exc.NoResultFound:
#         raise errors.NotFoundInDBError(f"Could not find user by uuid: {uuid}")
#     logger.debug(f"Returning: {got_user}")
#     if not got_user:
#         raise errors.NotFoundInDBError(f"User {user_uuid} not found in DB")
#     return got_user


def get(db: Session, user_uuid: UUID | str) -> user_models.UserTbl:
    start_time = time.time()
    stmt = select(user_models.UserTbl).where(
        user_models.UserTbl.id == user_uuid
    )
    try:
        got_user = db.execute(stmt).scalars().one()
    except exc.NoResultFound:
        raise errors.NotFoundInDBError(
            f"Could not find user by uuid: {user_uuid}"
        )
    logger.warning(f"DB user fetch: {time.time() - start_time:.3f} seconds")
    logger.debug(f"Returning: {got_user}")
    return got_user


def get_by_email(db: Session, email: str) -> user_models.UserTbl:
    stmt = select(user_models.UserTbl).where(
        user_models.UserTbl.email == email
    )
    try:
        got_user = db.execute(stmt).scalars().one()
    except exc.NoResultFound:
        raise errors.NotFoundInDBError(
            f"Could not find user by email: {email}"
        )
    logger.debug(f"Returning: {got_user}")
    return got_user


def get_all(db: Session):
    stmt = select(user_models.UserTbl).order_by(user_models.UserTbl.email)
    result = db.execute(stmt).scalars().all()
    logger.debug(f"result: {result}")
    return result


def create(
    db: Session,
    email: str,
    image: str | None = None,
    username: str | None = None,
) -> user_models.UserTbl:
    """Create a user"""
    logger.debug(f"Creating new user: {email}")
    new_user_account = user_models.UserTbl(
        email=email, image=image, username=username
    )
    logger.debug(f"Adding new user: {new_user_account}")
    db.add(new_user_account)
    logger.debug(f"Flushing new user.")
    db.flush()
    return new_user_account


def create_oauth_account(
    db: Session,
    user_uuid: str | UUID,
    provider_id: OAuthProviderValue | OAuthProvider,
    provider_user_id: str,
) -> user_models.UserAccountTbl:
    """Create an oauth account for the target user."""
    # Enforce valid enum by loading as enum instance
    provider_id = OAuthProvider(provider_id).value
    logger.debug(
        f"Creating new oauth account: {user_uuid=} {provider_id=}, {provider_user_id=}"
    )
    new_oauth_account = user_models.UserAccountTbl(
        user_id=user_uuid,
        provider_id=provider_id,
        provider_user_id=provider_user_id,
    )
    logger.debug(f"Adding new oauth_account: {new_oauth_account}")
    db.add(new_oauth_account)
    return new_oauth_account


# Moved sessions handling to REDIS
# def create_session(db, user_uuid: str | UUID):
#     new_session = user_models.UserSessionsTbl(user_id=user_uuid)
#     logger.debug(f"db.add() new user session: {new_session}")
#     db.add(new_session)
#     return new_session
