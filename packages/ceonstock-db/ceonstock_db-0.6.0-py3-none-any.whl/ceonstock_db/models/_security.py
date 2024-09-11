from uuid import uuid4
from datetime import datetime, timedelta

from sqlalchemy import (
    String,
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


# For temoporary security tokens
def get_valid_until():
    valid_until = datetime.now() + timedelta(hours=1)
    return valid_until


# TODO move this to REDIS DB (more appropriate for ephemeral data, avoids needing cron jobs
# to delete expired data)
class EmailVerificationTokenTbl(Base):
    __tablename__ = "email_verification_token"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    user_account_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_account.uuid", ondelete="CASCADE"),
    )
    email_to_verify: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=get_valid_until
    )
    # user: Mapped["UserAccountTbl"] = relationship()
