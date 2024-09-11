import logging
from dotenv import load_dotenv

load_dotenv("../secret/.env")

from ceonstock_db.database import SessionLocal
from ceonstock_db import db_setup
from ceonstock_db import crud
from ceonstock_db import schemas

# Make logging visible
root_logger = logging.getLogger()
root_logger.addHandler(logging.StreamHandler())
root_logger.setLevel("INFO")

logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()
    logger.info(f"Connected to db session: {db}")
    with db as session:
        db_setup.reset.reset_schema(session)

        # Create user_roles
        db_setup.setup_user_roles.push_to_db(session)

        # Read and print
        print()
        db_setup.setup_user_roles.print_user_roles(session)
        db_setup.setup_user_roles.print_permissions(session)
        db_setup.setup_user_roles.print_granted_permissions(session)

        # Create default users
        print()
        logger.info("Creating default users...")
        db_setup.users.create_default_users(session)


if __name__ == "__main__":
    main()
