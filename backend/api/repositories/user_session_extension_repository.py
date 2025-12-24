"""
Repository for UserSessionExtension database operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from api.models.user_session_extension_db import UserSessionExtensionDB
from api.models.user_session_extension import UserSessionExtensionCreate, UserSessionExtensionUpdate
from typing import Optional
from datetime import datetime


class UserSessionExtensionRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_user_id(self, user_id: str) -> Optional[UserSessionExtensionDB]:
        """Get user session extension by user ID"""
        result = await self.db_session.execute(
            select(UserSessionExtensionDB).where(UserSessionExtensionDB.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: str, last_module_id: Optional[str] = None,
                     language_preference: str = "en", default_module_id: Optional[str] = None) -> UserSessionExtensionDB:
        """Create a new user session extension"""
        db_user_session = UserSessionExtensionDB(
            user_id=user_id,
            last_module_id=last_module_id,
            language_preference=language_preference,
            default_module_id=default_module_id
        )
        self.db_session.add(db_user_session)
        await self.db_session.commit()
        await self.db_session.refresh(db_user_session)
        return db_user_session

    async def update(self, user_id: str, update_data: UserSessionExtensionUpdate) -> Optional[UserSessionExtensionDB]:
        """Update user session extension"""
        stmt = (
            update(UserSessionExtensionDB)
            .where(UserSessionExtensionDB.user_id == user_id)
            .values(**update_data.dict(exclude_unset=True))
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

        # Return the updated record
        return await self.get_by_user_id(user_id)

    async def update_last_module(self, user_id: str, module_id: str) -> Optional[UserSessionExtensionDB]:
        """Update the last accessed module for a user"""
        stmt = (
            update(UserSessionExtensionDB)
            .where(UserSessionExtensionDB.user_id == user_id)
            .values(last_module_id=module_id, last_access_time=datetime.now())
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

        return await self.get_by_user_id(user_id)

    async def update_language_preference(self, user_id: str, language: str) -> Optional[UserSessionExtensionDB]:
        """Update the language preference for a user"""
        stmt = (
            update(UserSessionExtensionDB)
            .where(UserSessionExtensionDB.user_id == user_id)
            .values(language_preference=language)
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

        return await self.get_by_user_id(user_id)

    async def delete(self, user_id: str) -> bool:
        """Delete user session extension"""
        stmt = delete(UserSessionExtensionDB).where(UserSessionExtensionDB.user_id == user_id)
        result = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return result.rowcount > 0