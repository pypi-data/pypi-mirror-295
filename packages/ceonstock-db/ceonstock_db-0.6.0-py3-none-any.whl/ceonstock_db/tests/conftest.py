import pytest
import logging
from ceonstock_db.tests import TestSessionLocal
from ceonstock_db import db_setup

# fixtures defined here in conftest.py can be used by the tests in any modules

logger = logging.getLogger(__name__)


# Making TestSessionLocal accessible via fixture so we don't have to
# manually import it to every test module
@pytest.fixture(scope="session")
def db_session():
    """Provides the database connection to be used for all testing.
    The schema is reset and the DB is empty by default.
    Use the other fixtures to provide testing data"""
    with TestSessionLocal() as session:
        engine = session.get_bind()
        logger.warning(f"Got session bind: {engine}")
        logger.warning(f"Got session engine uri: {engine.url}")
        db_setup.reset.reset_schema(session)
    return TestSessionLocal


@pytest.fixture()
def default_db_session(db_session):
    """Delete existing DB entries and reset the testing state"""
    with db_session() as session:
        # TODO delete/reset entries from other tests?
        # Refactor db_setup/testing and a master db_setup.testing.insert_testing_data
        logger.warning("Fixture resetting DB entries...")
        db_setup.reset.clear_data(session)
        db_setup.access_control.push_to_db(session)
        db_setup.users.create_default_users(session)
        db_setup.project.push_to_db(session)
    return db_session


@pytest.fixture()
def empty_db_session(db_session):
    """Provides an empty DB with only the schema initialized"""
    with db_session() as session:
        logger.warning("Fixture clearing data")
        db_setup.reset.clear_data(session)
        # Refactor db_setup/testing and a master db_setup.testing.insert_testing_data
    return db_session
