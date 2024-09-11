import os
import logging
from dotenv import load_dotenv
from ceonstock_db import database

load_dotenv()
logger = logging.getLogger(__name__)

TEST_DB_URI = os.environ["TEST_DB_URI"]
connect_args = {}  # No ssl for local dev connecton

TestSessionLocal = database.create_local_session_maker(
    TEST_DB_URI, connect_args=connect_args
)
