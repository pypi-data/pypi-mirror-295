import logging
import pytest
from uuid import UUID

from sqlalchemy.orm import Session

from ceonstock_db import crud
from ceonstock_db import models
from ceonstock_db import schemas
from ceonstock_db import errors

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel("INFO")


NEW_USER_CREATE = schemas.UserAccountCreate(
    email="newly_created_user@hotmail.com", password="123"
)


# Create a simple, regular user
def test_token_create_success(default_db_session):
    with default_db_session() as session:
        # reset_schema(session)
        # TODO get test user(s) from... a 'fixutre'?
        user = crud.user.get_by_email(session, "admin@ceonstock.com")
        logger.info(f"Got user for testing email verification tokens: {user.email}")

        token = crud.security.create_email_verification_token(
            session, str(user.uuid), user.email
        )
        logger.info(f"Created token: {token.__dict__}")
        assert token.user_account_uuid == user.uuid


# TODO add test for email changing (token redemption process is hte same, but a token must be
# created that sets the email to a value different from the current email)


def test_token_redeem_success(default_db_session):
    # This test assumes handling a newly registered user that has not yet confirmed their email
    with default_db_session() as session:
        # TODO get test user(s) from... a 'fixutre'?
        user = crud.user.get_by_email(session, "admin@ceonstock.com")
        user.email_is_confirmed = False
        logger.info(
            f"Got user for testing email verification tokens: {user.email}, email_is_confirmed: {user.email_is_confirmed}"
        )

        # Create a token for the user
        token = crud.security.create_email_verification_token(
            session, str(user.uuid), user.email
        )
        logger.info(f"Created token: {token.__dict__}")
        assert token.user_account_uuid == user.uuid

        # Redeem the token
        logger.info(f"Redeeming email verification token...")
        crud.security.redeem_email_verification_token(session, str(token.uuid))

        # Confirm that user's email was updated to match the email in the token
        # And that email_is_confirmed is True
        assert user.email == token.email_to_verify
        assert user.email_is_confirmed == True
