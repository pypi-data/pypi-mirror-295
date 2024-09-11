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


# ------------------
# -- Child tables --
# ------------------
class UserStripeTbl(Base):
    # Map an app user to their stripe customer id.
    __tablename__ = "user_stripe"

    user_account_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
    )
    stripe_customer_id: Mapped[str] = mapped_column(String(30), unique=True)
