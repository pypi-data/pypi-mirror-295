import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

DEFAULT_CONNECT_ARGS = {"sslmode": "require"}
connect_args_local_docker = {}


# For fastapi to create db sessions for each request
def create_local_session_maker(db_uri: str, connect_args=None) -> sessionmaker:
    if connect_args == None:
        connect_args = DEFAULT_CONNECT_ARGS
    logger.warning(
        "TODO make sure to use connect_args with sslmode require in production"
    )
    logger.warning(f"{connect_args=}")
    engine = create_engine(
        # DB_URI, connect_args=connect_args, pool_pre_ping=True
        db_uri,
        connect_args=connect_args,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


def test_db_engine_connection(engine):
    logger.info("Testing DB connection...")
    logger.info(f"URI: {engine.url}")
    conn = engine.connect()
    conn.close()
    logger.info(f"Closed test connection: {engine.url}")


def test_db_session_connection(session):
    engine = session.get_bind()
    logger.info("Testing DB connection...")
    logger.info(f"URI: {engine.url}")
    conn = engine.connect()
    conn.close()
    logger.info(f"Closed test connection: {engine.url}")


def get_db_uri_from_session(session):
    engine = session.get_bind()
    return engine.url
