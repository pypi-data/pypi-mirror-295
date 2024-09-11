from uuid import uuid4
from datetime import date, timedelta

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

# from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from .base import Base


def get_valid_until():
    valid_until = date.today() + timedelta(days=30)
    return valid_until


class SubmissionTbl(Base):
    __tablename__ = "submission"

    # TODO remove id(renamed), replace with uuid.
    # Maintain id for legacy reasons until production API is ready to be updated
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid4,
        server_default=text("gen_random_uuid()"),
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )
    user_account_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE")
    )
    project_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("project.uuid", ondelete="CASCADE")
    )
    validated: Mapped[bool] = mapped_column(
        Boolean, server_default="false", nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=get_valid_until
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    project: Mapped["ProjectTbl"] = relationship()
