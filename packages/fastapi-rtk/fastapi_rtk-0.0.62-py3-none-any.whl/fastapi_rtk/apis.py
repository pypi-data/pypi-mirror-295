from typing import List

from fastapi import Depends, HTTPException, Request, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .api import BaseApi, ModelRestApi, SQLAInterface
from .api.interface import PARAM_BODY_QUERY
from .db import UserDatabase, get_user_db
from .decorators import expose, login_required
from .globals import g
from .models import Api, Permission, PermissionApi, Role, User
from .routers import get_auth_router, get_oauth_router
from .schemas import (
    GeneralResponse,
    InfoResponse,
    UserCreate,
    UserRead,
    UserReadWithStringRoles,
    UserUpdate,
)

__all__ = [
    "AuthApi",
    "InfoApi",
    "PermissionsApi",
    "PermissionViewApi",
    "RolesApi",
    "UsersApi",
    "ViewsMenusApi",
]


class PermissionViewApi(ModelRestApi):
    resource_name = "permissionview"
    datamodel = SQLAInterface(PermissionApi)
    max_page_size = 200
    base_permissions = ["can_get", "can_info"]


class ViewsMenusApi(ModelRestApi):
    resource_name = "viewsmenus"
    datamodel = SQLAInterface(Api)
    max_page_size = 200
    base_permissions = ["can_get", "can_info"]


class PermissionsApi(ModelRestApi):
    resource_name = "permissions"
    datamodel = SQLAInterface(Permission)
    max_page_size = 200
    base_permissions = ["can_get", "can_info"]


class RolesApi(ModelRestApi):
    resource_name = "roles"
    datamodel = SQLAInterface(Role)
    max_page_size = 200


class InfoApi(BaseApi):
    resource_name = "info"

    security_level_apis = [
        "PermissionsApi",
        "RolesApi",
        "UsersApi",
        "ViewsMenusApi",
        "PermissionViewApi",
    ]
    excluded_apis = ["InfoApi", "AuthApi"]

    def __init__(self):
        expose("/")(self.get_info)
        login_required(self.get_info)
        super().__init__()

    def get_info(self):
        if not self.toolkit:
            return []

        apis = self.cache.get("get_info", [])
        if apis:
            return apis

        for api in self.toolkit.apis:
            if api.__class__.__name__ in self.excluded_apis:
                continue

            api_info = {}
            api_info["name"] = api.resource_name.capitalize()
            api_info["icon"] = "Table" if hasattr(api, "datamodel") else ""
            api_info["permission_name"] = api.__class__.__name__
            api_info["path"] = api.resource_name
            api_info["type"] = "table" if hasattr(api, "datamodel") else "default"
            api_info["level"] = (
                "security"
                if api.__class__.__name__ in self.security_level_apis
                else "default"
            )
            apis.append(api_info)

        self.cache["get_info"] = apis
        return apis


class UsersApi(ModelRestApi):
    resource_name = "users"
    datamodel = SQLAInterface(User)
    list_exclude_columns = ["password", "hashed_password"]
    show_exclude_columns = ["password", "hashed_password"]
    add_exclude_columns = [
        "active",
        "last_login",
        "login_count",
        "fail_login_count",
        "created_on",
        "changed_on",
        "oauth_accounts",
    ]
    edit_exclude_columns = [
        "username",
        "last_login",
        "login_count",
        "fail_login_count",
        "created_on",
        "changed_on",
        "oauth_accounts",
    ]
    label_columns = {"password": "Password"}

    def pre_info(
        self,
        info: InfoResponse,
        permissions: List[str],
        session: AsyncSession | Session,
    ):
        for col in info.edit_columns:
            if col.name == "password":
                col.required = False

    def pre_add(self, item: User, params: PARAM_BODY_QUERY):
        try:
            UserCreate.model_validate(item, from_attributes=True)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors()
            )

    def pre_update(self, item: User, params: PARAM_BODY_QUERY):
        try:
            UserUpdate.model_validate(item, from_attributes=True)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors()
            )

    async def post_add(self, item: User, params: PARAM_BODY_QUERY):
        await g.current_app.security.update_user(
            user=item,
            user_update=UserUpdate(password=item.password),
            session=params.query.session,
        )
        await params.query.refresh(item)

    async def post_update(self, item: User, params: PARAM_BODY_QUERY):
        if params.body.password:
            await g.current_app.security.update_user(
                user=item,
                user_update=UserUpdate(password=params.body.password),
                session=params.query.session,
            )
        await params.query.refresh(item)


class AuthApi(BaseApi):
    resource_name = "auth"

    def __init__(self):
        super().__init__()
        if g.config.get("AUTH_LOGIN_COOKIE", True):
            self.router.include_router(
                get_auth_router(
                    g.auth.cookie_backend,
                    g.auth.fastapi_users.get_user_manager,
                    g.auth.fastapi_users.authenticator,
                )
            )
        if g.config.get("AUTH_LOGIN_JWT"):
            self.router.include_router(
                get_auth_router(
                    g.auth.jwt_backend,
                    g.auth.fastapi_users.get_user_manager,
                    g.auth.fastapi_users.authenticator,
                ),
                prefix="/jwt",
            )
        if g.config.get("AUTH_USER_REGISTRATION"):
            self.router.include_router(
                g.auth.fastapi_users.get_register_router(UserRead, UserCreate),
            )
        if g.config.get("AUTH_USER_RESET_PASSWORD"):
            self.router.include_router(
                g.auth.fastapi_users.get_reset_password_router(),
            )
        if g.config.get("AUTH_USER_VERIFY"):
            self.router.include_router(
                g.auth.fastapi_users.get_verify_router(UserRead),
            )

        oauth_clients = g.config.get("OAUTH_CLIENTS") or g.config.get(
            "OAUTH_PROVIDERS", []
        )
        for client in oauth_clients:
            oauth_client = client["oauth_client"]
            associate_by_email = client.get("associate_by_email", False)
            on_after_register = client.get("on_after_register", None)

            self.router.include_router(
                get_oauth_router(
                    oauth_client=oauth_client,
                    backend=g.auth.cookie_backend,
                    get_user_manager=g.auth.fastapi_users.get_user_manager,
                    state_secret=g.auth.secret_key,
                    redirect_url=g.config.get("OAUTH_REDIRECT_URI"),
                    associate_by_email=associate_by_email,
                    on_after_register=on_after_register,
                ),
            )

    @expose(
        "/user",
        methods=["GET"],
        response_model=UserReadWithStringRoles,
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            }
        },
    )
    def get_user():
        if not g.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token or inactive user.",
            )
        user_data = UserRead.model_validate(g.user)
        user_data.roles = [role.name for role in g.user.roles]
        return user_data

    @expose(
        "/user",
        methods=["PUT"],
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            }
        },
    )
    async def update_user(
        request: Request,
        user_update: UserUpdate,
        user_db: UserDatabase = Depends(get_user_db),
    ):
        if not g.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token or inactive user.",
            )
        user_manager = next(g.auth.get_user_manager(user_db))
        await user_manager.update(user_update, g.user, safe=True, request=request)
        return GeneralResponse(detail="User updated successfully.")
