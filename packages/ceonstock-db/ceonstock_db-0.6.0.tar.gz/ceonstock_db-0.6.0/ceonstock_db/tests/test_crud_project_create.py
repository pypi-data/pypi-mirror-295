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
logger.setLevel("DEBUG")

# TODO split this module into three test modules
# test_user_create
# test_user_update
# test_user_get (e.g. get by role (admin, affiliate) etc)


def add_project(
    db: Session, project_to_create: schemas.ProjectCreate
) -> models.ProjectTbl:
    logger.info(f"Creating project: {project_to_create.title}")
    project_in_db = crud.project.create(db, project_to_create)
    logger.debug(f"Successfully added project: {project_in_db}")
    return project_in_db


def delete_project(db: Session, User):
    raise NotImplementedError


@pytest.fixture()
def project_to_create(default_db_session) -> schemas.ProjectCreate:
    default_owner_email = "admin@ceonstock.com"
    with default_db_session() as session:
        default_owner = crud.user.get_by_email(session, default_owner_email)
        logger.debug(f"Got default owner: {default_owner}")
    project_to_create = schemas.ProjectCreate(
        title="Test Project CRUD",
        description="This project was created to test the DB CRUD api",
        proj_inputs=[{"testinput1": "aaa"}],
        owner_uuid=default_owner.uuid,
    )
    return project_to_create


# Create a simple, regular user
def test_create_project_success(default_db_session, project_to_create):
    with default_db_session() as session:
        # reset_schema(session)
        new_project_in_db = add_project(session, project_to_create)
        got_project = crud.project.get(session, new_project_in_db.uuid)
        logger.info(f"Got new project in db: {got_project}")
