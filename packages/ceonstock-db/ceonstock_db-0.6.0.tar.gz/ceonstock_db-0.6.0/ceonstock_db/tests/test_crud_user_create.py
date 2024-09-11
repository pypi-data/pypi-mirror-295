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

# TODO split this module into three test modules
# test_user_create
# test_user_update
# test_user_get (e.g. get by role (admin, affiliate) etc)


def add_user(default_db_session, user_to_create) -> models.UserAccountTbl:
    logger.info(f"Creating user: {user_to_create.email}")
    user_in_db = crud.user.create(default_db_session, user_to_create)
    logger.debug(f"Successfully added user: {user_in_db}")
    return user_in_db


def delete_user(db: Session, User):
    raise NotImplementedError


# TODO test_add_user_fail_already_exists():
# TODO test_add_user_with_role_success():
# TODO test_add_user_with_role_fail():

# Include deletes in the 'create' module?
# TODO test_delete_user():

# Different module for getting/updating information.
# TODO test_get_user():
# TODO test_get_user_by_email():

NEW_USER_CREATE = schemas.UserAccountCreate(
    email="newly_created_user@hotmail.com", password="123"
)


# Create a simple, regular user
def test_add_user_success(default_db_session):
    with default_db_session() as session:
        # reset_schema(session)
        new_user_in_db = add_user(session, NEW_USER_CREATE)
        got_user = crud.user.get_by_email(session, new_user_in_db.email)
        logger.info(f"Got new user in db: {got_user}")


# Create the same user twice and confirm that a AlreadyExistsInDBError is thrown
def test_add_user_already_exists(default_db_session):
    with default_db_session() as session:
        # reset_schema(session)
        new_user_in_db = add_user(session, NEW_USER_CREATE)
        got_user = crud.user.get_by_email(session, new_user_in_db.email)
        logger.info(f"Got new user in db: {got_user}")
        logger.info("Creating user again...")
        with pytest.raises(errors.AlreadyExistsInDBError):
            add_user(session, NEW_USER_CREATE)
    logger.warning(
        "TODO: Confirm no side-effects on failure? E.g. no child tables created"
    )
