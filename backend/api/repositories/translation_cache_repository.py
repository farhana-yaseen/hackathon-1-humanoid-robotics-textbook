"""
Repository for TranslationCache database operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, and_
from api.models.translation_cache_db import TranslationCacheDB
from typing import Optional
from datetime import datetime, timezone


class TranslationCacheRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_hash_and_language(self, content_hash: str, target_language: str) -> Optional[TranslationCacheDB]:
        """Get cached translation by content hash and language"""
        result = await self.db_session.execute(
            select(TranslationCacheDB)
            .where(
                and_(
                    TranslationCacheDB.content_hash == content_hash,
                    TranslationCacheDB.target_language == target_language
                )
            )
            .where(TranslationCacheDB.expires_at > datetime.now(timezone.utc))
        )
        return result.scalar_one_or_none()

    async def create(self, content_hash: str, target_language: str, translated_content: str,
                     expires_at: datetime, original_content_length: Optional[int] = None) -> TranslationCacheDB:
        """Create a new cached translation"""
        db_cache = TranslationCacheDB(
            content_hash=content_hash,
            target_language=target_language,
            translated_content=translated_content,
            expires_at=expires_at,
            original_content_length=original_content_length
        )
        self.db_session.add(db_cache)
        await self.db_session.commit()
        await self.db_session.refresh(db_cache)
        return db_cache

    async def update(self, content_hash: str, target_language: str, translated_content: str,
                     expires_at: datetime) -> Optional[TranslationCacheDB]:
        """Update cached translation"""
        stmt = (
            update(TranslationCacheDB)
            .where(
                and_(
                    TranslationCacheDB.content_hash == content_hash,
                    TranslationCacheDB.target_language == target_language
                )
            )
            .values(
                translated_content=translated_content,
                expires_at=expires_at
            )
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

        # Return the updated record
        return await self.get_by_hash_and_language(content_hash, target_language)

    async def delete(self, content_hash: str, target_language: str) -> bool:
        """Delete cached translation"""
        stmt = (
            delete(TranslationCacheDB)
            .where(
                and_(
                    TranslationCacheDB.content_hash == content_hash,
                    TranslationCacheDB.target_language == target_language
                )
            )
        )
        result = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return result.rowcount > 0

    async def delete_expired(self) -> int:
        """Delete all expired cache entries"""
        stmt = delete(TranslationCacheDB).where(TranslationCacheDB.expires_at <= datetime.now(timezone.utc))
        result = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return result.rowcount

    async def get_cached_translation(self, content_hash: str, target_language: str) -> Optional[str]:
        """Get cached translation content by hash and language if not expired"""
        cache_entry = await self.get_by_hash_and_language(content_hash, target_language)
        if cache_entry:
            return cache_entry.translated_content
        return None

    async def delete_expired_entries(self) -> int:
        """Delete all expired cache entries - alias for delete_expired for compatibility"""
        return await self.delete_expired()