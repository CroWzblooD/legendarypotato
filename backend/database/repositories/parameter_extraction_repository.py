"""
Parameter Extraction Repository - Data access layer for parameter_extractions table.
"""
import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import ParameterExtraction
from database.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class ParameterExtractionRepository(BaseRepository[ParameterExtraction]):
    """Repository for ParameterExtraction operations."""
    
    async def create(
        self,
        conversation_id: str,
        user_message: str,
        extracted_params: Dict[str, Any],
        inferred_params: Optional[Dict[str, Any]] = None,
        confidence_score: float = 0.0,
        missing_required: Optional[Dict[str, Any]] = None
    ) -> ParameterExtraction:
        """Create a new parameter extraction record."""
        extraction = ParameterExtraction(
            conversation_id=self.to_uuid(conversation_id),
            user_message=user_message,
            extracted_params=extracted_params,
            inferred_params=inferred_params,
            confidence_score=confidence_score,
            missing_required=missing_required
        )
        
        await self._add_and_flush(extraction)
        logger.info(f"Logged parameter extraction: confidence={confidence_score:.2f}, inferred={len(inferred_params or {})}")
        return extraction
