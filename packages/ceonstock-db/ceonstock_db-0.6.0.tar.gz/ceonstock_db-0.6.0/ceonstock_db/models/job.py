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

from ceonstock_db.models import ProjectTbl

from .base import Base


def get_valid_until():
    valid_until = date.today() + timedelta(days=30)
    return valid_until


class JobTbl(Base):
    __tablename__ = "job"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
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
    submission_uuid: Mapped[UUID] = mapped_column(
        # UUID(as_uuid=True),
        UUID(as_uuid=True),
        ForeignKey("submission.uuid", ondelete="SET NULL"),
    )
    # TODO allow type checking to enforce enum?
    job_type: Mapped[str] = mapped_column(String(30), nullable=False)
    # job_type: Mapped[CstockJob.job_types] = mapped_column(String(30), nullable=False)
    # ForeignKey("submission.id", ondelete="SET NULL"),
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    ended_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    success: Mapped[Boolean] = mapped_column(Boolean, nullable=True)

    project: Mapped["ProjectTbl"] = relationship()
    user_account: Mapped["UserTbl"] = relationship()


class JobProgressTbl(Base):
    __tablename__ = "job_progress"

    job_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    assigned_to_node: Mapped[str] = mapped_column(String, nullable=True)
    assigned_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    started_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    create_job_inputs_start: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    create_job_inputs_end: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    prepare_files_start: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    prepare_files_end: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    render_submit_start: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    render_submit_end: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    wait_for_render_start: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    wait_for_render_end: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    upload_outputs_start: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    upload_outputs_end: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


# TODO setup this by converting TIMESTAMP objects to strings then to datetime objects?
"""
job_progress_tbl.d.latest_timestamp = (
    func.max(
        [
            job_progress_tbl.c.started_at,
            job_progress_tbl.c.render_submit_start,
            job_progress_tbl.c.render_complete_confirmed,
            job_progress_tbl.c.upload_outputs_start,
            job_progress_tbl.c.ended_at,
        ]
    )
).label("latest_timestamp")
"""
# Can be late accessed as job_progress_tbl.d.latest_timestamp as though it were a real column
