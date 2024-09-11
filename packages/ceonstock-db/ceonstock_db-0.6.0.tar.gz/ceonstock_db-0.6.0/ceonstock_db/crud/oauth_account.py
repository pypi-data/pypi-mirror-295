# Test
import logging
from enum import Enum
from typing_extensions import Literal
from typing import get_args
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import exc
from sqlalchemy import select

from ceonstock_db.models import user as user_models

# from ceonstock_db.auth import security
from ceonstock_db import errors

logger = logging.getLogger(__name__)


class OAuthProvider(str, Enum):
    GOOGLE = "google"
    GITHUB = "github"
    EMAIL = "email"


# Created to type hint for allowing string values for static type checking
OAuthProviderValue = Literal["google", "github", "email"]

# Enforce that type hinting is synch'd with enum
assert set(get_args(OAuthProviderValue)) == {
    member.value for member in OAuthProvider
}


def get(
    db: Session,
    provider_id: OAuthProviderValue | OAuthProvider,
    provider_user_id: str,
) -> user_models.UserAccountTbl:
    if isinstance(provider_id, OAuthProvider):
        provider_id = provider_id.value
    stmt = select(user_models.UserAccountTbl).where(
        user_models.UserAccountTbl.provider_id == str(provider_id),
        user_models.UserAccountTbl.provider_user_id == str(provider_user_id),
    )
    try:
        got_user_account = db.execute(stmt).scalars().one()
    except exc.NoResultFound:
        raise errors.NotFoundInDBError(
            f"Could not find user_account: {provider_id=}, {provider_user_id=}"
        )
    logger.debug(f"Returning: {got_user_account}")
    return got_user_account
