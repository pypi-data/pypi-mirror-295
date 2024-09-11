import json
from typing import TYPE_CHECKING, Literal, Optional

from fastapi_users.exceptions import UserNotExists
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .const import logger
from .db import UserDatabase, db
from .globals import g
from .models import Api, Permission, Role, User
from .schemas import RoleSchema, UserCreate, UserReadWithPassword, UserUpdate
from .utils import safe_call
from .version import __version__

__all__ = ["SecurityManager"]

if TYPE_CHECKING:
    from .fastapi_react_toolkit import FastAPIReactToolkit


class SecurityManager:
    """
    The SecurityManager class provides functions to manage users, roles, permissions, and APIs.
    """

    toolkit: Optional["FastAPIReactToolkit"]

    def __init__(self, toolkit: Optional["FastAPIReactToolkit"] = None) -> None:
        self.toolkit = toolkit

    """
    -----------------------------------------
         USER MANAGER FUNCTIONS
    -----------------------------------------
    """

    async def get_user(
        self,
        email_or_username: str,
        session: AsyncSession | Session | None = None,
    ):
        """
        Gets the user with the specified email or username.

        Args:
            email_or_username (str): The email or username of the user.
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            User | None: The user object if found, else None.
        """
        try:
            if session:
                return await self._get_user(session, email_or_username)

            async with db.session() as session:
                return await self._get_user(session, email_or_username)
        except UserNotExists:
            return None

    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        roles: list[str] | None = None,
        session: AsyncSession | Session | None = None,
    ):
        """
        Creates a new user with the given information.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The password of the user.
            first_name (str, optional): The first name of the user. Defaults to "".
            last_name (str, optional): The last name of the user. Defaults to "".
            roles (list[str] | None, optional): The roles assigned to the user. Defaults to None.
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            User: The created user object.

        Raises:
            SomeException: Description of the exception raised, if any.
        """

        if session:
            return await self._create_user(
                session,
                username,
                email,
                password,
                first_name,
                last_name,
                roles,
            )

        async with db.session() as session:
            return await self._create_user(
                session, username, email, password, first_name, last_name, roles
            )

    async def update_user(
        self,
        user: User,
        user_update: UserUpdate,
        session: AsyncSession | Session | None = None,
    ):
        """
        Updates the specified user with the given information.

        Args:
            user (User): The user to update.
            update_dict (UserUpdate): The schema object with the updated information.
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            User: The updated user object.

        Raises:
            SomeException: Description of the exception raised, if any.
        """
        if session:
            return await self._update_user(session, user, user_update)

        async with db.session() as session:
            return await self._update_user(session, user, user_update)

    async def create_role(
        self, name: str, session: AsyncSession | Session | None = None
    ):
        """
        Creates a new role with the given name.

        Args:
            name (str): The name of the role to create.
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            Role: The created role object.

        Raises:
            SomeException: Description of the exception raised, if any.
        """
        if session:
            return await self._create_role(session, name)

        async with db.session() as session:
            return await self._create_role(session, name)

    async def reset_password(
        self,
        user: User,
        new_password: str,
        session: AsyncSession | Session | None = None,
    ):
        """
        Resets the password of the specified user.

        Args:
            user (User): The user whose password is to be reset.
            new_password (str): The new password to set.
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            User: The user object with the updated password.

        Raises:
            SomeException: Description of the exception raised, if any.
        """
        if session:
            return await self._reset_password(session, user, new_password)

        async with db.session() as session:
            return await self._reset_password(session, user, new_password)

    async def _get_user(self, session: AsyncSession | Session, email_or_username: str):
        manager = next(g.auth.get_user_manager(UserDatabase(session, User)))
        try:
            return await manager.get_by_email(email_or_username)
        except UserNotExists:
            return await manager.get_by_username(email_or_username)

    async def export_data(
        self,
        data: Literal["users", "roles"],
        type: Literal["json", "csv"] = "json",
        session: AsyncSession | Session | None = None,
    ):
        """
        Exports the specified data to a file.

        Args:
            data (Literal["users", "roles"]): The data to export (users or roles).
            type (Literal["json", "csv"], optional): The type of file to export the data to. Defaults to "json".
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            str: The exported data in JSON or CSV format.

        Raises:
            SomeException: Description of the exception raised, if any.
        """
        if session:
            match data:
                case "users":
                    return await self._export_users(session, type)
                case "roles":
                    return await self._export_roles(session, type)

        async with db.session() as session:
            match data:
                case "users":
                    return await self._export_users(session, type)
                case "roles":
                    return await self._export_roles(session, type)

    async def _create_user(
        self,
        session: AsyncSession | Session,
        username: str,
        email: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        roles: list[str] | None = None,
    ):
        manager = next(g.auth.get_user_manager(UserDatabase(session, User)))
        return await manager.create(
            UserCreate(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            ),
            roles,
        )

    async def _update_user(
        self,
        session: AsyncSession | Session,
        user: User,
        user_update: UserUpdate,
    ):
        manager = next(g.auth.get_user_manager(UserDatabase(session, User)))
        return await manager.update(user_update, user)

    async def _create_role(
        self,
        session: AsyncSession | Session,
        name: str,
    ):
        role = Role(name=name)
        session.add(role)
        await safe_call(session.commit())
        return role

    async def _reset_password(
        self, session: AsyncSession | Session, user: User, new_password: str
    ):
        manager = next(g.auth.get_user_manager(UserDatabase(session, User)))
        token = await manager.forgot_password(user)
        return await manager.reset_password(token, new_password)

    async def _export_users(
        self, session: AsyncSession | Session, type: Literal["json", "csv"] = "json"
    ):
        stmt = select(User)
        users = await safe_call(session.scalars(stmt))
        user_dict = {}
        for user in users:
            user_dict[user.username] = UserReadWithPassword.model_validate(
                user
            ).model_dump()
        if type == "json":
            return json.dumps(user_dict, indent=4)

        csv_data = "Username,Data\n"
        for username, data in user_dict.items():
            csv_data += f"{username},{data}\n"
        return csv_data

    async def _export_roles(
        self, session: AsyncSession | Session, type: Literal["json", "csv"] = "json"
    ):
        stmt = select(Role)
        roles = await safe_call(session.scalars(stmt))
        role_dict = {}
        for role in roles:
            # TODO: Change result
            role_dict[role.name] = RoleSchema.model_validate(role).model_dump()
        if type == "json":
            return json.dumps(role_dict, indent=4)

        csv_data = "Role,Data\n"
        for role, data in role_dict.items():
            csv_data += f"{role},{','.join(data)}\n"
        return csv_data

    """
    -----------------------------------------
         SECURITY FUNCTIONS
    -----------------------------------------
    """

    async def cleanup(self, session: AsyncSession | Session | None = None):
        """
        Cleanup unused permissions from apis and roles.

        Returns:
            None
        """
        if session:
            return await self._cleanup(session)

        async with db.session() as session:
            return await self._cleanup(session)

    async def _cleanup(self, session: AsyncSession | Session):
        if not self.toolkit:
            raise Exception(
                "FastAPIReactToolkit instance not provided, you must provide it to use this function."
            )

        api_permission_tuples = (
            g.config.get("ROLES") or g.config.get("FAB_ROLES", {})
        ).values()
        apis = [api.__class__.__name__ for api in self.toolkit.apis]
        permissions = self.toolkit.total_permissions()
        for api_permission_tuple in api_permission_tuples:
            for api, permission in api_permission_tuple:
                apis.append(api)
                permissions.append(permission)

        # Clean up unused permissions
        unused_permissions = await safe_call(
            session.scalars(select(Permission).where(~Permission.name.in_(permissions)))
        )
        for permission in unused_permissions:
            logger.info(f"DELETING PERMISSION {permission} AND ITS ASSOCIATIONS")
            await safe_call(session.delete(permission))

        # Clean up unused apis
        unused_apis = await safe_call(
            session.scalars(select(Api).where(~Api.name.in_(apis)))
        )
        for api in unused_apis:
            logger.info(f"DELETING API {api} AND ITS ASSOCIATIONS")
            await safe_call(session.delete(api))

        await safe_call(session.commit())
