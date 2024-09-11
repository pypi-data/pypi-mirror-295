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

from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from .base import Base


class ProjectTbl(Base):
    __tablename__ = "project"

    uuid = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )
    owner_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String)
    proj_inputs = mapped_column(JSON, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    owner: Mapped["UserTbl"] = relationship(back_populates="user_projects")
