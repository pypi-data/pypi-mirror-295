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


# TODO separate 'user_account' (logins via oauth) and 'user'
# Parent table for the user entity
class UserTbl(Base):
    __tablename__ = "user"

    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        unique=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    username: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    image: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    # user_profile: Mapped["UserProfileTbl"] = relationship(
    #     back_populates="user"
    # )
    user_projects: Mapped[list["ProjectTbl"]] = relationship(
        back_populates="owner"
    )
    user_roles: Mapped[list["RoleTbl"]] = relationship(  # type: ignore
        secondary=access_control.granted_user_role_table
    )
    accounts: Mapped[list["UserAccountTbl"]] = relationship(
        back_populates="user"
    )
    reusable_preview_credits: Mapped[list["ReusablePreviewTokenTbl"]] = (
        relationship(back_populates="user")
    )

    def __repr__(self):
        return f"User(id={self.id!r}, email={self.email!r})"


# ------------------
# -- Child tables --
# ------------------


# One user may have multiple 'accounts' (login methods e.g. Google, Github, Email)
class UserAccountTbl(Base):
    __tablename__ = "oauth_account"

    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        unique=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
    )
    provider_id: Mapped[str] = mapped_column(String(255))
    provider_user_id: Mapped[str] = mapped_column(String(255))
    # refresh_token: Mapped[str] = mapped_column(nullable=True)
    # access_token: Mapped[str] = mapped_column(nullable=True)
    # expires_at: Mapped[int] = mapped_column(nullable=True)
    # id_token: Mapped[str] = mapped_column(nullable=True)
    # scope: Mapped[str] = mapped_column(nullable=True)
    # session_state: Mapped[str] = mapped_column(nullable=True)
    # token_type: Mapped[str] = mapped_column(nullable=True)

    user: Mapped["UserTbl"] = relationship(back_populates="accounts")


# Moved sessions to redis storage.
# class UserSessionsTbl(Base):
#     __tablename__ = "session"

#     # id: Mapped[int] = mapped_column(primary_key=True)
#     id: Mapped[str] = mapped_column(
#         primary_key=True,
#         nullable=False,
#         index=True,
#         unique=True,
#         server_default=text("gen_random_uuid()"),
#     )
#     user_id: Mapped[UUID] = mapped_column(
#         ForeignKey("user.id", ondelete="CASCADE"), nullable=False
#     )
#     expires_at: Mapped[DateTime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now()
#     )
#     user: Mapped["UserTbl"] = relationship()
