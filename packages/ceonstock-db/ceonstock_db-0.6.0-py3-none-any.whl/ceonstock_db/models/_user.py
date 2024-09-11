from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    text,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ceonstock_db.models.base import Base
from . import access_control


# Parent table for the user entity
class UserAccountTbl(Base):
    __tablename__ = "user_account"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        unique=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email_is_confirmed: Mapped[bool] = mapped_column(Boolean, server_default="f")
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user_profile: Mapped["UserProfileTbl"] = relationship(back_populates="user")
    user_projects: Mapped[list["ProjectTbl"]] = relationship(back_populates="owner")
    user_roles: Mapped[list["UserRoleTbl"]] = relationship(  # type: ignore
        secondary=access_control.granted_user_role_table
    )
    user_login: Mapped["UserLoginTbl"] = relationship(back_populates="user")
    reusable_preview_credits: Mapped[list["ReusablePreviewTokenTbl"]] = relationship(
        back_populates="user_account"
    )

    def __repr__(self):
        return f"User(uuid={self.uuid!r}, email={self.email!r})"


# ------------------
# -- Child tables --
# ------------------


class UserLoginTbl(Base):
    __tablename__ = "user_login"

    user_account_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_account.uuid", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(String(60))
    password_recovery_token: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
    )
    user: Mapped["UserAccountTbl"] = relationship(back_populates="user_login")

    # In this case we don't want to add user_login to UserTbl,
    # so don't back_populate?
    # user: Mapped["UserAccountTbl"] = relationship()
    # user: Mapped["UserTbl"] = relationship(back_populates="user_login")


class UserProfileTbl(Base):
    __tablename__ = "user_profile"

    user_account_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_account.uuid", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
    )
    username: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    avatar: Mapped[Optional[str]] = mapped_column(String(255))
    first_name: Mapped[Optional[str]] = mapped_column(String(20))
    last_name: Mapped[Optional[str]] = mapped_column(String(20))

    user: Mapped["UserAccountTbl"] = relationship(back_populates="user_profile")
    # DoB? How-to Date (not DateTime)
    # WebSite?
    # IMDB?
