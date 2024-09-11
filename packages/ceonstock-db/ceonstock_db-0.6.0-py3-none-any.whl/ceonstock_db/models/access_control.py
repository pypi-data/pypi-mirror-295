from uuid import uuid4
from typing import Optional

# import sqlalchemy
from sqlalchemy import (
    Index,
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    text,
)
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ceonstock_db.models.base import Base

# Permissions setup following the advice of:
# https://vertabelo.com/blog/user-authentication-module/
# With SQLAlchemy's recommended implementation for mant-to-many relationships, using association tables:
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many

# --------------------
# -- Mapping Tables --
# --------------------
# To create many:many relationships between entities we use a third table for mapping

# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
granted_permission_table = Table(
    # Assigns permissions to user_roles
    "granted_permission",
    Base.metadata,
    Column("role_uuid", ForeignKey("role.uuid"), primary_key=True),
    Column("permission_uuid", ForeignKey("permission.uuid"), primary_key=True),
    # Index(
    #     "idx_granted_permission", "user_role_uuid", "permission_uuid", unique=True
    # ),  # Needed?
    UniqueConstraint(  # Don't allow entries with the same user_role/permission combination
        "role_uuid", "permission_uuid", name="_granted_permission_uc"
    ),
)

granted_user_role_table = Table(
    "granted_user_role",
    Base.metadata,
    Column("user_uuid", ForeignKey("user.id"), primary_key=True),
    Column("role_uuid", ForeignKey("role.uuid"), primary_key=True),
    UniqueConstraint(  # Don't allow entries with the same account/role combination (no duplicate entries)
        "user_uuid", "role_uuid", name="_granted_user_role_uc"
    ),
)


# --------------------
# -- Entity Tables --
# --------------------
# Lookup table
# A user role which can be assigned to a user to grant associated
# permissions.
class RoleTbl(Base):
    __tablename__ = "role"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(String(20), unique=False)
    description: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=True
    )
    permissions: Mapped[list["PermissionTbl"]] = relationship(
        secondary=granted_permission_table, back_populates="user_roles"
    )


# Lookup table
# Specific permissions which are checked for to perform an action
class PermissionTbl(Base):
    __tablename__ = "permission"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(String(30), unique=False)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    user_roles: Mapped[list["RoleTbl"]] = relationship(
        secondary=granted_permission_table, back_populates="permissions"
    )
