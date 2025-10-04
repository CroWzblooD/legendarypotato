"""
Pydantic models for type safety and validation.
Defines schemas for all educational tools and student data.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class MessageRole(str, Enum):
    """Message role in conversation."""
    USER = "user"
    ASSISTANT = "assistant"


class ToolType(str, Enum):
    """Available educational tools."""
    NOTE_MAKER = "note_maker"
    FLASHCARD_GENERATOR = "flashcard_generator"
    CONCEPT_EXPLAINER = "concept_explainer"


class TeachingStyle(str, Enum):
    """Teaching style preferences."""
    DIRECT = "direct"
    SOCRATIC = "socratic"
    VISUAL = "visual"
    FLIPPED_CLASSROOM = "flipped_classroom"


class EmotionalState(str, Enum):
    """Student emotional states."""
    FOCUSED = "focused"
    ANXIOUS = "anxious"
    CONFUSED = "confused"
    TIRED = "tired"
    MOTIVATED = "motivated"


# ============================================================================
# BASE MODELS
# ============================================================================

class ChatMessage(BaseModel):
    """Single message in conversation."""
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None
    
    model_config = {"use_enum_values": True}


class UserInfo(BaseModel):
    """Student profile information."""
    user_id: str = Field(..., description="Unique student identifier")
    name: str = Field(..., description="Student's full name")
    grade_level: str = Field(..., description="Current grade level")
    learning_style_summary: str = Field(..., description="Learning preferences summary")
    emotional_state_summary: str = Field(..., description="Current emotional state")
    mastery_level_summary: str = Field(..., description="Current mastery level description")
    teaching_style: Optional[TeachingStyle] = Field(default=TeachingStyle.DIRECT)
    
    model_config = {"use_enum_values": True}


# ============================================================================
# TOOL INPUT SCHEMAS
# ============================================================================

class NoteMakerInput(BaseModel):
    """Input schema for Note Maker tool."""
    user_info: UserInfo
    chat_history: List[ChatMessage]
    topic: str = Field(..., description="Main topic for note generation")
    subject: str = Field(..., description="Academic subject area")
    note_taking_style: Literal["outline", "bullet_points", "narrative", "structured"]
    include_examples: bool = True
    include_analogies: bool = False


class FlashcardGeneratorInput(BaseModel):
    """Input schema for Flashcard Generator tool."""
    user_info: UserInfo
    topic: str = Field(..., description="Topic for flashcard generation")
    count: int = Field(..., ge=1, le=20, description="Number of flashcards")
    difficulty: Literal["easy", "medium", "hard"]
    include_examples: bool = True
    subject: str = Field(..., description="Academic subject area")
    
    @field_validator('count')
    @classmethod
    def validate_count(cls, v: int) -> int:
        if not 1 <= v <= 20:
            raise ValueError("Count must be between 1 and 20")
        return v


class ConceptExplainerInput(BaseModel):
    """Input schema for Concept Explainer tool."""
    user_info: UserInfo
    chat_history: List[ChatMessage]
    concept_to_explain: str = Field(..., description="Specific concept to explain")
    current_topic: str = Field(..., description="Broader topic context")
    desired_depth: Literal["basic", "intermediate", "advanced", "comprehensive"]


# ============================================================================
# TOOL OUTPUT SCHEMAS
# ============================================================================

class NoteSection(BaseModel):
    """Single section in generated notes."""
    title: str
    content: str
    key_points: List[str] = []
    examples: List[str] = []
    analogies: List[str] = []


class NoteMakerOutput(BaseModel):
    """Output schema for Note Maker tool."""
    topic: str
    title: str
    summary: str
    note_sections: List[NoteSection]
    key_concepts: List[str]
    connections_to_prior_learning: List[str] = []
    visual_elements: List[Dict[str, Any]] = []
    practice_suggestions: List[str] = []
    source_references: List[str] = []
    note_taking_style: str


class Flashcard(BaseModel):
    """Single flashcard."""
    title: str
    question: str
    answer: str
    example: Optional[str] = None


class FlashcardGeneratorOutput(BaseModel):
    """Output schema for Flashcard Generator tool."""
    flashcards: List[Flashcard]
    topic: str
    adaptation_details: str
    difficulty: str


class ConceptExplainerOutput(BaseModel):
    """Output schema for Concept Explainer tool."""
    explanation: str
    examples: List[str] = []
    related_concepts: List[str] = []
    visual_aids: List[str] = []
    practice_questions: List[str] = []
    source_references: List[str] = []


# ============================================================================
# ORCHESTRATOR MODELS
# ============================================================================

class ExtractedParameters(BaseModel):
    """Parameters extracted from conversation."""
    tool_type: ToolType
    parameters: Dict[str, Any]
    confidence: float = Field(ge=0.0, le=1.0, description="Extraction confidence score")
    missing_required: List[str] = []
    inferred_params: Dict[str, str] = {}  # Track which params were inferred
    
    model_config = {"use_enum_values": True}


class ChatRequest(BaseModel):
    """Request to chat endpoint."""
    message: str = Field(..., description="User's message")
    user_info: UserInfo
    conversation_id: Optional[str] = None
    chat_history: List[ChatMessage] = []


class ToolResponse(BaseModel):
    """Response from tool execution."""
    tool_type: ToolType
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None
    
    model_config = {"use_enum_values": True}


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    conversation_id: str
    message: str
    tool_response: Optional[ToolResponse] = None
    extracted_parameters: Optional[ExtractedParameters] = None
    needs_clarification: bool = False
    clarification_question: Optional[str] = None


# ============================================================================
# STATE MODELS (for LangGraph)
# ============================================================================

class OrchestratorState(BaseModel):
    """State object passed through LangGraph workflow."""
    # Input
    user_message: str
    user_info: UserInfo
    chat_history: List[ChatMessage]
    conversation_id: str
    
    # Processing
    intent: Optional[ToolType] = None
    extracted_params: Optional[ExtractedParameters] = None
    validation_passed: bool = False
    tool_input: Optional[Dict[str, Any]] = None
    
    # Output
    tool_response: Optional[ToolResponse] = None
    final_message: Optional[str] = None
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    
    # Metadata
    processing_steps: List[str] = []
    errors: List[str] = []
    
    model_config = {
        "arbitrary_types_allowed": True,
        "use_enum_values": True
    }
