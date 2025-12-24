"""
Repository for ModuleAccessLog database operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc
from api.models.module_access_log_db import ModuleAccessLogDB
from typing import Optional, List
from datetime import datetime
import uuid


class ModuleAccessLogRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, user_id: str, module_id: str, session_id: Optional[str] = None,
                     position: int = 0) -> ModuleAccessLogDB:
        """Create a new module access log entry"""
        db_log = ModuleAccessLogDB(
            user_id=user_id,
            module_id=module_id,
            session_id=session_id,
            position=position
        )
        self.db_session.add(db_log)
        await self.db_session.commit()
        await self.db_session.refresh(db_log)
        return db_log

    async def get_last_accessed_module(self, user_id: str) -> Optional[str]:
        """Get the last accessed module ID for a user"""
        result = await self.db_session.execute(
            select(ModuleAccessLogDB.module_id)
            .where(ModuleAccessLogDB.user_id == user_id)
            .order_by(desc(ModuleAccessLogDB.access_time))
            .limit(1)
        )
        row = result.fetchone()
        return row[0] if row else None

    async def get_user_access_history(self, user_id: str, limit: int = 10) -> List[ModuleAccessLogDB]:
        """Get the access history for a user"""
        result = await self.db_session.execute(
            select(ModuleAccessLogDB)
            .where(ModuleAccessLogDB.user_id == user_id)
            .order_by(desc(ModuleAccessLogDB.access_time))
            .limit(limit)
        )
        return result.scalars().all()

    async def update_position(self, log_id: uuid.UUID, position: int) -> Optional[ModuleAccessLogDB]:
        """Update the position for a module access log entry"""
        # Note: Since we don't have a direct update method in the model, we'll need to query and update
        # For now, this is a placeholder - in practice, you'd typically create a new entry with the updated position
        pass

    async def get_recent_accesses(self, user_id: str, module_id: str, limit: int = 5) -> List[ModuleAccessLogDB]:
        """Get recent accesses for a specific user and module"""
        result = await self.db_session.execute(
            select(ModuleAccessLogDB)
            .where(
                and_(
                    ModuleAccessLogDB.user_id == user_id,
                    ModuleAccessLogDB.module_id == module_id
                )
            )
            .order_by(desc(ModuleAccessLogDB.access_time))
            .limit(limit)
        )
        return result.scalars().all()