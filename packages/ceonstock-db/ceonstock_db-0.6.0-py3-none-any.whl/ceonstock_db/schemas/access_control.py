from enum import Enum


class UserRoleOption(str, Enum):
    VERIFIED_USER = "verified"
    ARTIST = "artist"
    AFFILIATE = "affiliate"
    ADMIN = "admin"


class PermissionOption(str, Enum):
    SUBMIT_PREVIEWS = "submit_preview"
    PURCHASE = "purchase"
    MANAGE_PROJECT = "manage_project"
    DELETE_PROJECT = "delete_project"
