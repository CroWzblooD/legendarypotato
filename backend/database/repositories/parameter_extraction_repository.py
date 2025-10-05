"""
Parameter Extraction Repository - Data access layer for parameter_extractions table.
This is CRITICAL - tracks the 40% of hackathon score (parameter extraction quality)!
"""
import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import ParameterExtraction

logger = logging.getLogger(__name__)


class ParameterExtractionRepository:
    """Repository for ParameterExtraction operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
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
            conversation_id=UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id,
            user_message=user_message,
            extracted_params=extracted_params,
            inferred_params=inferred_params,
            confidence_score=confidence_score,
            missing_required=missing_required
        )
        
        self.session.add(extraction)
        await self.session.flush()
        
        logger.info(f"Logged parameter extraction: confidence={confidence_score:.2f}, inferred={len(inferred_params or {})}")
        return extraction
    
    async def get_by_conversation(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[ParameterExtraction]:
        """Get parameter extractions for a conversation."""
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        result = await self.session.execute(
            select(ParameterExtraction)
            .where(ParameterExtraction.conversation_id == uuid_id)
            .order_by(ParameterExtraction.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_confidence(
        self,
        min_confidence: float = 0.0,
        max_confidence: float = 1.0,
        limit: int = 100
    ) -> List[ParameterExtraction]:
        """Get extractions filtered by confidence range."""
        result = await self.session.execute(
            select(ParameterExtraction)
            .where(
                ParameterExtraction.confidence_score >= min_confidence,
                ParameterExtraction.confidence_score <= max_confidence
            )
            .order_by(ParameterExtraction.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_average_confidence(self) -> float:
        """Calculate average confidence score across all extractions."""
        result = await self.session.execute(
            select(func.avg(ParameterExtraction.confidence_score))
        )
        avg_confidence = result.scalar_one_or_none()
        return avg_confidence if avg_confidence else 0.0
    
    async def get_inference_stats(self) -> Dict[str, Any]:
        """
        Get statistics about parameter inference.
        This is KEY for hackathon scoring!
        """
        # Total extractions
        total_result = await self.session.execute(
            select(func.count(ParameterExtraction.extraction_id))
        )
        total = total_result.scalar_one()
        
        # Extractions with inferred params
        inferred_result = await self.session.execute(
            select(func.count(ParameterExtraction.extraction_id))
            .where(ParameterExtraction.inferred_params.isnot(None))
        )
        with_inference = inferred_result.scalar_one()
        
        # Average confidence
        avg_confidence = await self.get_average_confidence()
        
        # High confidence extractions (>= 0.8)
        high_conf_result = await self.session.execute(
            select(func.count(ParameterExtraction.extraction_id))
            .where(ParameterExtraction.confidence_score >= 0.8)
        )
        high_confidence_count = high_conf_result.scalar_one()
        
        return {
            "total_extractions": total,
            "with_inference": with_inference,
            "inference_percentage": (with_inference / total * 100) if total > 0 else 0,
            "average_confidence": avg_confidence,
            "high_confidence_count": high_confidence_count,
            "high_confidence_percentage": (high_confidence_count / total * 100) if total > 0 else 0
        }
    
    async def get_recent_extractions(self, limit: int = 10) -> List[ParameterExtraction]:
        """Get most recent parameter extractions."""
        result = await self.session.execute(
            select(ParameterExtraction)
            .order_by(ParameterExtraction.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
