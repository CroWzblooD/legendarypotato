"""
Base repository with common functionality.
Eliminates duplicate UUID conversion logic across all repositories.
"""
from typing import TypeVar, Generic
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository class with shared utilities."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    @staticmethod
    def to_uuid(value: str | UUID) -> UUID:
        """
        Convert string to UUID if needed.
        Handles both string and UUID inputs gracefully.
        """
        return UUID(value) if isinstance(value, str) else value
    
    async def _add_and_flush(self, obj: T) -> T:
        """
        Add object to session and flush.
        Common pattern used across all repositories.
        """
        self.session.add(obj)
        await self.session.flush()
        return obj
