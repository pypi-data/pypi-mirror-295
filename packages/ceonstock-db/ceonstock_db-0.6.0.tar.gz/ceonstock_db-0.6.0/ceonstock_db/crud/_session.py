# Test
import logging
from datetime import datetime, timedelta
from uuid import UUID
from datetime import datetime
from datetime import timezone

from sqlalchemy.orm import Session
from sqlalchemy import exc
from sqlalchemy import select


from ceonstock_db import models
from ceonstock_db.auth import security
from ceonstock_db import errors

# TODO can proj_crud safely auto-fetch the SessionLocal without it needing to be passed?
# from db.engine import SessionLocal

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")


def get(db: Session, session_id: str) -> models.user.UserSessionsTbl:
    logger.info(f"Fetching user for session: {session_id=}")
    stmt = select(models.user.UserSessionsTbl).where(
        models.user.UserSessionsTbl.id == session_id
    )
    try:
        got_session = db.execute(stmt).scalars().one()
    except exc.NoResultFound:
        raise errors.NotFoundInDBError(
            f"Could not find session for session_id"
        )
    logger.info(f"got session: {got_session=}")
    expired = got_session.expires_at <= datetime.now(tz=timezone.utc)
    # Get the session
    logger.info(f"{expired=}")
    if expired:
        # TODO create appropriate exception
        logger.warning("TODO: Delete expired sessions")
        raise Exception("Session expired")
    return got_session


# TODO move sessions to redis?
def create(db: Session, user_id: str) -> models.user.UserSessionsTbl:
    # Create new job entry
    user_id = str(user_id)
    time_to_live = timedelta(days=30)
    expires_at = datetime.now(tz=timezone.utc) + time_to_live
    logger.info(f"{expires_at=}")
    new_session = models.user.UserSessionsTbl(
        user_id=user_id, expires_at=expires_at
    )
    db.add(new_session)
    db.flush()
    logger.info(f"Created new_session: {new_session.__dict__}")
    return new_session
