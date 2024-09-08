# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from datetime import datetime
from typing import Union

import jwt
from fastapi import HTTPException
from fastapi import status as st
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import false

from ..conf import config
from ..crud import BaseCRUD
from .models import Token, User
from .schemas import (
    TokenDataSchema,
    TokenRefreshCreate,
    UserCreateForm,
    UserResetPassForm,
    UserSchema,
)
from .securities import ALGORITHM, get_password_hash, verify_password


async def authenticate(
    session: AsyncSession,
    name: str,
    password: str,
) -> Union[User, bool]:
    if user := await User.get_by_username(session, username=name):
        return (
            user if verify_password(password, user.hashed_password) else False
        )
    return False


class TokenCRUD(BaseCRUD):

    async def retention_by_user(self, user_id: int):
        db_tokens: list[Token] = await Token.get_active_by_user(
            self.async_session, user_id
        )
        info: list[str] = []
        for record in db_tokens:
            if (datetime.now() - record.created_at).days > 1:
                info.append(record.id)

        if info:
            await self.async_session.execute(
                delete(Token).where(Token.id.in_(info))
            )
            await self.async_session.flush()
            await self.async_session.commit()

    async def update_logout(self, refresh_token: str):
        db_tokens = await Token.get_by_refresh(
            self.async_session, token=refresh_token
        )
        if db_tokens:
            rs = await self.async_session.execute(
                update(Token)
                .where(Token.get_by_refresh == refresh_token)
                .values(status=false())
                .returning(Token.access_token, Token.refresh_token)
            )
            await self.async_session.flush()
            await self.async_session.commit()
            return rs
        return []

    async def create(self, token: TokenRefreshCreate):
        db_token = Token(
            user_id=token.user_id,
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            status=token.status,
        )
        self.async_session.add(db_token)
        await self.async_session.flush()
        await self.async_session.commit()
        await self.async_session.refresh(db_token)
        return db_token


class UserCRUD(BaseCRUD):

    async def change_password(self, user: UserResetPassForm) -> UserSchema:
        db_user = await authenticate(
            self.async_session,
            name=user.username,
            password=user.old_password,
        )
        if db_user is None:
            raise HTTPException(
                status_code=st.HTTP_400_BAD_REQUEST,
                detail="User not found with old password",
            )

        encrypted_password = get_password_hash(user.new_password)
        db_user.password = encrypted_password
        await self.async_session.flush()
        await self.async_session.commit()
        await self.async_session.refresh(db_user)

        return UserSchema.model_validate(db_user)

    async def create_by_form(self, user: UserCreateForm) -> UserSchema:
        # NOTE: Validate by username value. By default, this will validate
        # from database with unique constraint.
        if await User.get_by_username(self.async_session, user.username):
            raise HTTPException(status_code=st.HTTP_409_CONFLICT)

        hashed_password = get_password_hash(user.password)
        db_user: User = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
        )
        self.async_session.add(db_user)

        # `flush`, communicates a series of operations to the database
        # (insert, update, delete). The database maintains them as pending
        # operations in a transaction. The changes aren't persisted
        # permanently to disk, or visible to other transactions until the
        # database receives a COMMIT for the current transaction (which is
        # what session.commit() does).
        # ---
        # docs: https://stackoverflow.com/questions/4201455/ -
        #   sqlalchemy-whats-the-difference-between-flush-and-commit
        await self.async_session.flush()

        # # `commit`, commits (persists) those changes to the database.
        await self.async_session.commit()

        # NOTE: persisted some changes for an object to the database and
        # need to use this updated object within the same method.
        await self.async_session.refresh(db_user)
        return UserSchema.model_validate(db_user)


async def verify_token(
    token: str,
    session: AsyncSession,
) -> TokenDataSchema | None:
    if await Token.get(session, token=token):
        return None

    try:
        payload = jwt.decode(
            token, config.OBSERVE_REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
        if username := payload.get("sub"):
            return TokenDataSchema(username=username)
        return None
    except jwt.InvalidTokenError:
        return None


async def add_blacklist_token(token: str, session: AsyncSession) -> None:
    payload = jwt.decode(
        token, config.OBSERVE_SECRET_KEY, algorithms=[ALGORITHM]
    )
    expires_at = datetime.fromtimestamp(payload.get("exp"))
    await Token.create(
        session,
        **{"token": token, "expires_at": expires_at},
    )
