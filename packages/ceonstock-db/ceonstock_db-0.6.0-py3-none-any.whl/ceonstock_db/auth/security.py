# Authentication
import os
import logging
from typing import Optional, List  # Extends data type inputs for fastapi
from datetime import datetime, timedelta

from ceonstock_db.crud import user as user_crud

# Moved inside functions to avoid dependencies when importing ceonstock_db
# from passlib.context import CryptContext
# from jose import JWTError, jwt

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def authenticate_credentials(db, email: str, unhashed_password: str):
    # Importing here to avoid dependencies when ceonstock_db is imported by render/submisssion servers
    from passlib.context import CryptContext
    from jose import JWTError, jwt

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # verify password
    saved_hash = user_crud.Login.get_saved_hash(db, email)
    logger.debug(f"got login for email: {email}:{saved_hash}")
    if not saved_hash:
        raise Exception(
            "Failed to find hashed_password in DB when trying to authenticate user credentials"
        )
    if pwd_context.verify(unhashed_password, saved_hash):
        user = user_crud.User.get_by_email(db, email)
        logger.debug(f"user: {user}")
        return user
    return None


def hash_password(password):
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


""" Not DB related. Move to API server code
def create_access_token(payload: dict):
    logger.debug(f"received payload: {payload}")
    restructured_data = {"sub": payload}
    logger.debug(f"restructured data: {restructured_data}")
    to_encode = restructured_data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    logger.debug(f"added 'exp' to data: {to_encode}")
    if not JWT_SECRET:
        msg = "Unable to create token due to missing ENV var: JWT_SECRET"
        logger.error(msg)
        raise Exception(msg)
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    logger.debug(f"encoded_jwt: {encoded_jwt}")
    return encoded_jwt
"""


# WIP remove api/website functionality from this module.
# def create_access_token_cookie(payload):
#     max_age_seconds = 60 * ACCESS_TOKEN_EXPIRE_MINUTES
#     access_token = create_access_token(payload)
#     domain = "localhost" if (os.getenv("ENV") == "DEV") else "ceonstock.com"
#     access_token_cookie = f"access_token={access_token}; Domain={domain}; Path=/; Max-Age={max_age_seconds}; HttpOnly"
#     logger.debug(
#         f"Created access token cookie with payload({payload}): {access_token_cookie}"
#     )
#     return access_token_cookie


# WIP remove api/website functionality from this module.
# def decode_access_token(token):
#     payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
#     logger.debug(f"Decoded token: {token}\nToken payload: {payload}")
#     return payload
