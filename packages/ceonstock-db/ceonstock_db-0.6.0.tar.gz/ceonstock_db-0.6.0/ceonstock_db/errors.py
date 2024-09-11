import logging
from sqlalchemy import exc
from psycopg2 import errors as psy_errors

logger = logging.getLogger(__name__)


class CstockDBError(Exception):
    pass


class NotFoundInDBError(CstockDBError):
    pass


class AlreadyExistsInDBError(CstockDBError):
    pass


def handle_sql_error(sql_error, msg=None):
    """Receives an SQL error and raises the appropriate custom error"""
    logger.debug("Handling error...")
    if isinstance(sql_error, exc.IntegrityError):
        logger.debug("Got IntegrityError...")
        _handle_sql_integrity_error(sql_error, msg=msg)
    raise sql_error


def _handle_sql_integrity_error(sql_integrity_error: exc.IntegrityError, msg=None):
    if isinstance(sql_integrity_error.orig, psy_errors.UniqueViolation):
        logger.debug("Got UniqueViolation...")
        default_msg = f"UniqueViolation: {sql_integrity_error}"
        message_to_raise = msg if msg else default_msg
        raise AlreadyExistsInDBError(message_to_raise)
    if isinstance(sql_integrity_error.orig, psy_errors.ForeignKeyViolation):
        default_msg = f"ForeignKeyViolation: {sql_integrity_error}"
        message_to_raise = msg if msg else default_msg
        logger.debug("Got ForeignKeyViolation...")
        raise NotFoundInDBError(message_to_raise)
    raise Exception(f"Unknown SQL Integrity error :O : {sql_integrity_error}")
