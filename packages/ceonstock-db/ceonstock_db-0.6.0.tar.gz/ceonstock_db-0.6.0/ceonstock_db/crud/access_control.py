import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from psycopg2.errors import UniqueViolation

from ceonstock_db import schemas
from ceonstock_db import models
from ceonstock_db import errors

logger = logging.getLogger(__name__)


# --------------
# User Roles
# --------------
def create_role(
    db: Session, user_role: schemas.UserRoleOption
) -> models.RoleTbl:
    logger.debug(f"Creating new user role: {user_role}")
    new_user_role = models.RoleTbl(name=user_role.value)
    logger.debug(f"Adding new user role to DB: {new_user_role}")
    db.add(new_user_role)

    # -- Commit Changes --
    try:
        db.commit()
        logger.debug(f"Committed new user role to db: {new_user_role.name}")
    except SQLAlchemyError as e:
        msg = f"Failed to create role {user_role}: {e}"
        errors.handle_sql_error(e, msg=msg)

    return new_user_role


def get_all_user_roles(db: Session) -> list[schemas.UserRoleOption]:
    stmt = select(models.RoleTbl).order_by(models.RoleTbl.name)
    result = db.execute(stmt).scalars().all()
    logger.debug(f"result: {result}")
    list_of_enum_instances = [
        schemas.UserRoleOption(user_role.name) for user_role in list(result)
    ]
    return list_of_enum_instances


# --------------
# Permisissions
# --------------
def create_permission(
    db: Session, permission_to_create: schemas.PermissionOption
) -> models.PermissionTbl:
    """Add a new permission to the database"""
    logger.debug(f"Creating new permission: {permission_to_create}")
    new_permission = models.PermissionTbl(name=permission_to_create.value)
    logger.debug(f"Adding new permission to db: {new_permission}")
    db.add(new_permission)

    # -- Commit Changes --
    db.commit()
    logger.debug(f"Committed new permission to db: {new_permission}")

    return new_permission


def get_all_permissions(
    db: Session,
) -> list[schemas.PermissionOption]:
    stmt = select(models.PermissionTbl).order_by(models.PermissionTbl.name)
    result = db.execute(stmt).scalars().all()
    logger.debug(f"result: {result}")
    list_of_enum_instances = [
        schemas.PermissionOption(permission.name)
        for permission in list(result)
    ]
    return list_of_enum_instances


def get_all_permissions_for_user_role(
    db: Session, user_role: schemas.UserRoleOption
) -> list[schemas.PermissionOption]:
    user_role_in_db = _get_user_role_in_db(db, user_role)
    permissions = user_role_in_db.permissions
    list_of_enums = [
        schemas.PermissionOption(permission.name) for permission in permissions
    ]
    return list_of_enums


# -----------
# Assignments
# -----------
def add_role_to_user(
    db: Session,
    user_account: models.user.UserAccountTbl,
    role_to_add: schemas.UserRoleOption,
):
    user_role_in_db: models.RoleTbl = _get_user_role_in_db(db, role_to_add)
    if user_role_in_db in user_account.user_roles:
        raise errors.AlreadyExistsInDBError(
            f"Tried to add already existing role ({role_to_add}) to user {user_account.email}"
        )
    user_account.user_roles.append(user_role_in_db)
    db.commit()


def add_permission_to_role(
    db: Session,
    user_role: schemas.UserRoleOption,
    permission_to_add: schemas.PermissionOption,
):
    logger.warning(
        f"Adding permission to role {user_role.value}: {permission_to_add.value}"
    )
    user_role_in_db = _get_user_role_in_db(db, user_role)
    permission_in_db = _get_permission_in_db(db, permission_to_add)
    if permission_in_db in user_role_in_db.permissions:
        # The UniqueConstraint on SQLAlchemy association table doesn't seem to raise an
        # error when making duplicate entries (but it does stop duplicates from being created)
        # Therefore, we explicitly check for and raise the error here.
        msg = f"Failed to add permissoin to role {user_role}: {permission_to_add} (already exists)"
        logger.error(msg)
        raise errors.AlreadyExistsInDBError(msg)
    user_role_in_db.permissions.append(permission_in_db)
    db.commit()


# ----
# Helper functions
# ----
# Not intended to be used by the user since the user
# will always pass/receive Enum instances.
def _get_user_role_in_db(
    db: Session, user_role: schemas.UserRoleOption
) -> models.RoleTbl:
    stmt = select(models.RoleTbl).where(models.RoleTbl.name == user_role.value)
    got_user_role = db.execute(stmt).scalars().one()
    logger.debug(f"Returning: {got_user_role}")
    return got_user_role


def _get_permission_in_db(
    db: Session, user_role: schemas.PermissionOption
) -> models.PermissionTbl:
    stmt = select(models.PermissionTbl).where(
        models.PermissionTbl.name == user_role.value
    )
    got_permission = db.execute(stmt).scalars().one()
    logger.debug(f"Returning: {got_permission}")
    return got_permission
