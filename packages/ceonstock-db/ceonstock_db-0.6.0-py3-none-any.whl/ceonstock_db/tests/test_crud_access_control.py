import pytest
import logging

from ceonstock_db import crud
from ceonstock_db import schemas
from ceonstock_db import errors

logger = logging.getLogger(__name__)


def test_create_user_role_success(empty_db_session):
    with empty_db_session() as session:
        existing_roles = crud.access_control.get_all_user_roles(session)
        logger.warning(f"Found existing user roles: {existing_roles}")
        role_to_create = schemas.UserRoleOption.VERIFIED_USER
        crud.access_control.create_role(session, role_to_create)
        session.commit()


def test_create_user_role_already_exists(empty_db_session):
    # First create the original entry
    with empty_db_session() as session:
        role_to_create = schemas.UserRoleOption.VERIFIED_USER
        crud.access_control.create_role(session, role_to_create)
        with pytest.raises(errors.AlreadyExistsInDBError):
            crud.access_control.create_role(session, role_to_create)


def test_add_permission_to_role_success(default_db_session):
    user_role = schemas.UserRoleOption.AFFILIATE
    permission = schemas.PermissionOption.SUBMIT_PREVIEWS
    with default_db_session() as session:
        crud.access_control.add_permission_to_role(session, user_role, permission)


def test_add_permission_to_role_already_exists(default_db_session):
    user_role = schemas.UserRoleOption.AFFILIATE
    permission = schemas.PermissionOption.SUBMIT_PREVIEWS
    with default_db_session() as session:
        crud.access_control.add_permission_to_role(session, user_role, permission)
        with pytest.raises(errors.AlreadyExistsInDBError):
            crud.access_control.add_permission_to_role(session, user_role, permission)


def test_get_permissions_for_user_role(default_db_session):
    user_role = schemas.UserRoleOption.VERIFIED_USER
    with default_db_session() as session:
        for user_role in schemas.UserRoleOption:
            list_of_permission_enums = (
                crud.access_control.get_all_permissions_for_user_role(
                    session, user_role
                )
            )
            logger.warning(
                f"Got permissions for role {user_role}:\n{list_of_permission_enums}"
            )
            for permission_enum in list_of_permission_enums:
                # Ensure returned type is an enum instance
                assert permission_enum in schemas.PermissionOption
