import logging
import pytest
from uuid import UUID

from sqlalchemy.orm import Session

from ceonstock_db import crud
from ceonstock_db import models
from ceonstock_db import schemas
from ceonstock_db import db_setup
from ceonstock_db.tests import TestSessionLocal

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel("INFO")

# TODO split this module into three test modules
# test_user_create
# test_user_update
# test_user_get (e.g. get by role (admin, affiliate) etc)


def add_user(db: Session, email: str, password: str) -> models.UserAccountTbl:
    user_to_create = schemas.user_schemas.UserAccountCreate(
        email=email, password=password
    )
    logger.info(f"Creating user: {user_to_create.email}")
    user_in_db = crud.user_crud.create(db, user_to_create)
    logger.debug(f"Successfully added user: {user_in_db}")
    return user_in_db


def delete_user(db: Session, User):
    raise NotImplementedError


# TODO test_get_user():
# TODO test_get_user_by_email():
# TODO test_delete_user():
# TODO test_add_user_fail_already_exists():
# TODO test_add_user_with_role_success():


@pytest.fixture
def existing_user():
    return models.UserAccountTbl(email="existing_user@gmail.com")


@pytest.fixture
def db_session():
    return TestSessionLocal()


# @pytest.fixture
# def empty_db_session(db_session: Session):
# """Reset the database to the testing state"""
# with db_session as session:
# db_setup.reset.reset_schema(session)
# return db_session


# @pytest.fixture(autouse=True)
@pytest.fixture
def default_db_session(db_session: Session):
    """Reset the database to the testing state"""
    with db_session as session:
        db_setup.reset.reset_schema(session)
        db_setup.users.create_default_users(session)
        # TODO setup default testing data
    return db_session


def test_add_user_success(default_db_session: Session):
    with default_db_session as session:
        # reset_schema(session)
        db_setup.reset.reset_schema(session)
        user_from_db = add_user(session, "added_user@hotmail.com", "123")
        add_user(session, "testuser3@hotmail.com", "123")
        got_user = crud.user_crud.get_by_email(session, user_from_db.email)
        logger.info(f"Read user: {got_user}")


def test_get_user_success(
    default_db_session: Session, existing_user: models.UserAccountTbl
):
    with default_db_session as session:
        got_user = crud.user_crud.get_by_email(session, existing_user.email)
    logger.info(f"Read got user: {got_user}")
    assert got_user != None
