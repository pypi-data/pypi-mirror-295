import logging
from sqlalchemy.orm import Session
from sqlalchemy import Sequence

from ceonstock_db import models
from ceonstock_db import crud

logger = logging.getLogger(__name__)


def test_get_all_users(default_db_session):
    with default_db_session() as session:
        users_in_db = crud.user.get_all(session)
        logger.warning(
            f"Successfully got {len(users_in_db)} users in db: {users_in_db}"
        )
