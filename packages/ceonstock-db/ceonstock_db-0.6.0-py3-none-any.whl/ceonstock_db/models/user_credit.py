from uuid import uuid4
from datetime import date, timedelta
from typing import Optional

from sqlalchemy import (
    Integer,
    String,
    JSON,
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
from ceonstock_db.models.user import UserAccountTbl


# Token to allow users to get free preview renders.
# They automatically refresh after a fixed time.
# Spent tokens are automatically refreshed if the user purchases the project.
class ReusablePreviewTokenTbl(Base):
    __tablename__ = "reusable_preview_token"
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid4,
        server_default=text("gen_random_uuid()"),
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )
    # Changed to regular id for compatability with oauth workflow, but left uuid naming convention to prevent
    # breakage
    user_account_uuid: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    # user_account_uuid: Mapped[UUID] = mapped_column(
    #     UUID(as_uuid=True),
    #     ForeignKey("user_account.uuid", ondelete="CASCADE"),
    #     nullable=False,
    # )
    # Remember the project which this token was last spent on.
    project_uuid: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project.uuid", ondelete="SET NULL"),
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    available_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user: Mapped["UserTbl"] = relationship(
        back_populates="reusable_preview_credits"
    )
