import logging
from typing import Literal

__all__ = ["logger"]

USER_TABLE = "ab_user"
ROLE_TABLE = "ab_role"
PERMISSION_TABLE = "ab_permission"
API_TABLE = "ab_view_menu"
PERMISSION_API_TABLE = "ab_permission_view"
ASSOC_PERMISSION_API_ROLE_TABLE = "ab_permission_view_role"
ASSOC_USER_ROLE_TABLE = "ab_user_role"
OAUTH_TABLE = "ab_oauth_account"

FASTAPI_RTK_TABLES = [
    USER_TABLE,
    ROLE_TABLE,
    PERMISSION_TABLE,
    API_TABLE,
    PERMISSION_API_TABLE,
    ASSOC_PERMISSION_API_ROLE_TABLE,
    ASSOC_USER_ROLE_TABLE,
    OAUTH_TABLE,
]

BASE_APIS = Literal[
    "AuthApi",
    "InfoApi",
    "PermissionsApi",
    "PermissionViewApi",
    "RolesApi",
    "UsersApi",
    "ViewsMenusApi",
]

EXCLUDE_ROUTES = Literal[
    "info", "download", "bulk", "get_list", "get", "post", "put", "delete"
]

PERMISSION_PREFIX = "can_"
DEFAULT_ADMIN_ROLE = "Admin"
DEFAULT_PUBLIC_ROLE = "Public"

DEFAULT_TOKEN_URL = "/api/v1/auth/jwt/login"
DEFAULT_SECRET = "SUPERSECRET"
DEFAULT_COOKIE_NAME = "dataTactics"
DEFAULT_STATIC_FOLDER = "static"
DEFAULT_TEMPLATE_FOLDER = "templates"

COOKIE_CONFIG_KEYS = [
    "cookie_name",
    "cookie_max_age",
    "cookie_path",
    "cookie_domain",
    "cookie_secure",
    "cookie_httponly",
    "cookie_samesite",
]
COOKIE_STRATEGY_KEYS = [
    "cookie_lifetime_seconds",
    "cookie_token_audience",
    "cookie_algorithm",
]
JWT_STRATEGY_KEYS = [
    "jwt_lifetime_seconds",
    "jwt_token_audience",
    "jwt_algorithm",
]
ROLE_KEYS = ["auth_admin_role", "auth_public_role"]


logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("DT_FASTAPI")
