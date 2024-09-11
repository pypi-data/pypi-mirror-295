import logging
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import exc
from sqlalchemy import select

from ceonstock_db import models

from ceonstock_db import errors

# TODO can proj_crud safely auto-fetch the SessionLocal without it needing to be passed?
# from db.engine import SessionLocal

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")


def get_customer(db: Session, user_uuid: UUID) -> models.stripe.UserStripeTbl:
    stmt = select(models.stripe.UserStripeTbl).where(
        models.stripe.UserStripeTbl.user_account_uuid == user_uuid
    )
    try:
        got_user = db.execute(stmt).scalars().one()
    except exc.NoResultFound:
        raise errors.NotFoundInDBError(
            f"Could not find user by uuid: {user_uuid}"
        )
    logger.debug(f"Returning: {got_user}")
    return got_user


def create_customer(
    db: Session, user_uuid: UUID, stripe_customer_id: str
) -> models.stripe.UserStripeTbl:
    logger.debug(
        f"Creating new stripe id: {stripe_customer_id} for user {user_uuid}"
    )
    new_stripe_customer = models.stripe.UserStripeTbl(
        user_account_uuid=user_uuid, stripe_customer_id=stripe_customer_id
    )
    logger.debug(f"Saving new stripe user: {new_stripe_customer}")
    db.add(new_stripe_customer)
    logger.debug(f"Added new stripe user to session: {new_stripe_customer}")

    # -- Commit Changes --
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        msg = f"Failed to commit changes (adding stripe customer) for new user: {user_uuid}"
        errors.handle_sql_error(e, msg=msg)
    logger.info(
        f"Committed new stripe customer to db: {new_stripe_customer.stripe_customer_id}"
    )

    return new_stripe_customer
