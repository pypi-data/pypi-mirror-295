import logging
from typing import Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy import exc
from sqlalchemy.orm import Session

from ceonstock_db import models
from ceonstock_db import errors

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def create_email_verification_token(
    db: Session, user_account_uuid: Union[UUID, str], email_to_verify: str
):
    logger.debug(f"Creating temporary security token...")
    new_token = models.security.EmailVerificationTokenTbl(
        user_account_uuid=user_account_uuid, email_to_verify=email_to_verify
    )
    db.add(new_token)
    logger.debug(f"Added new token to session: {new_token}")

    # Commit the changes and return the new token
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        msg = f"Failed to commit changes (creating token) for user: {user_account_uuid}"
        logger.error(msg)
        errors.handle_sql_error(e, msg=msg)
    except Exception as e:
        logger.error("Unknown exception")
        raise e
    return new_token


def get_email_verification_token(db: Session, token_uuid: Union[UUID, str]):
    # Get the token from the database
    stmt = select(models.security.EmailVerificationTokenTbl).where(
        models.security.EmailVerificationTokenTbl.uuid == token_uuid
    )
    token = db.execute(stmt).scalars().first()
    if not token:
        raise errors.NotFoundInDBError(
            f"Email verification token not found in db: {token_uuid}"
        )
    return token


def redeem_email_verification_token(db: Session, token_uuid: Union[UUID, str]):
    # TODO check that token is not expired
    """
    Executes 'email is verified' actions.
    - Update the user's main email address
    - Mark the user email as confirmed <--------
    - TODO assing verified user role <- TODO don't need both of these? Better to jsut use roles?
    - Delete the email-verifcation token.
    """
    # Get the token from the database
    stmt = select(models.security.EmailVerificationTokenTbl).where(
        models.security.EmailVerificationTokenTbl.uuid == token_uuid
    )
    token = db.execute(stmt).scalars().first()
    if not token:
        raise errors.NotFoundInDBError(
            f"Email verification token not found in db: {token_uuid}"
        )

    logger.debug(f"Getting user account tbl...")
    stmt = select(models.user.UserAccountTbl).where(
        models.user.UserAccountTbl.uuid == token.user_account_uuid
    )
    user_account = db.execute(stmt).scalars().first()
    if not user_account:
        raise errors.NotFoundInDBError(
            f"User not found in db for email verification token {token_uuid}: User({token.user_account_uuid})"
        )

    # Update the user fields
    user_account.email = token.email_to_verify
    user_account.email_is_confirmed = True

    logger.warning("Deleting used token...")
    db.delete(token)

    # -- Commit Changes --
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        msg = f"Failed to commit changes (verifying user email) for user: {user_account.email}"
        errors.handle_sql_error(e, msg=msg)
    logger.info(
        f"Committed changes to db (verified email) for user: {user_account.email}"
    )
