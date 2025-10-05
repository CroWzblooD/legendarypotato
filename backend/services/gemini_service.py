"""
Gemini AI service for intelligent parameter extraction and content generation.
Handles all interactions with Google's Gemini API.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from google import generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

from models.schemas import (
    ToolType, 
    ChatMessage, 
    UserInfo,
    ExtractedParameters,
    TeachingStyle,
    EmotionalState
)

logger = logging.getLogger(__name__)


def clean_json_response(text: str) -> str:
    """Clean JSON response from Gemini, removing markdown code blocks."""
    text = text.strip()
    # Remove ```json and ``` markers
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini service with API key."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required!")
        
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
        
        genai.configure(api_key=api_key)
        
        # LangChain Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            max_output_tokens=max_tokens,
            google_api_key=api_key
        )
        
        # Direct Gemini model for function calling
        self.model = genai.GenerativeModel(model_name)
        
        logger.info(f"Gemini service initialized with model: {model_name}")
    
    async def classify_intent(
        self, 
        message: str, 
        chat_history: List[ChatMessage],
        user_info: UserInfo
    ) -> ToolType:
        """
        Classify user intent to determine which educational tool to use.
        
        Args:
            message: Current user message
            chat_history: Previous conversation messages
            user_info: Student profile information
            
        Returns:
            ToolType enum indicating which tool to use
        """
        history_text = "\n".join([
            f"{msg.role if isinstance(msg.role, str) else msg.role.value}: {msg.content}" 
            for msg in chat_history[-5:]  # Last 5 messages for context
        ])
        
        prompt = f"""You are an expert educational assistant. Analyze the student's message and determine which educational tool they need.

Student Profile:
- Name: {user_info.name}
- Grade: {user_info.grade_level}
- Mastery Level: {user_info.mastery_level_summary}
- Emotional State: {user_info.emotional_state_summary}

Conversation History:
{history_text}

Current Message: "{message}"

Available Tools:
1. note_maker - For creating study notes, summaries, or study guides
2. flashcard_generator - For creating practice questions, flashcards, or quiz material
3. concept_explainer - For explaining concepts, answering "what is" or "how does" questions

Classification Rules:
- "notes", "summary", "study guide", "write down" → note_maker
- "flashcards", "questions", "quiz", "practice", "test me" → flashcard_generator
- "explain", "what is", "how does", "why", "understand", "confused about" → concept_explainer

Return ONLY the tool name (note_maker, flashcard_generator, or concept_explainer).
"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            tool_name = response.content.strip().lower()
            
            # Map to ToolType enum
            tool_mapping = {
                "note_maker": ToolType.NOTE_MAKER,
                "flashcard_generator": ToolType.FLASHCARD_GENERATOR,
                "concept_explainer": ToolType.CONCEPT_EXPLAINER,
            }
            
            tool = tool_mapping.get(tool_name)
            if not tool:
                # Default fallback based on keywords
                if any(word in message.lower() for word in ["note", "summary", "study guide"]):
                    tool = ToolType.NOTE_MAKER
                elif any(word in message.lower() for word in ["flashcard", "question", "quiz", "practice"]):
                    tool = ToolType.FLASHCARD_GENERATOR
                else:
                    tool = ToolType.CONCEPT_EXPLAINER
            
            logger.info(f"Intent classified as: {tool.value}")
            return tool
            
        except Exception as e:
            logger.error(f"Error in intent classification: {e}")
            # Default to concept explainer as safest option
            return ToolType.CONCEPT_EXPLAINER
    
    async def extract_parameters(
        self,
        message: str,
        chat_history: List[ChatMessage],
        user_info: UserInfo,
        tool_type: ToolType
    ) -> ExtractedParameters:
        """
        Extract parameters required for the identified tool from conversation.
        
        Uses multi-layer extraction:
        1. Explicit extraction (directly stated)
        2. Contextual inference (from conversation)
        3. Student profile adaptation
        4. Smart defaults
        
        Args:
            message: Current user message
            chat_history: Previous conversation
            user_info: Student profile
            tool_type: Which tool we're extracting for
            
        Returns:
            ExtractedParameters with all params and metadata
        """
        logger.info(f"Extracting parameters for {tool_type.value}")
        
        # Build conversation context
        history_text = "\n".join([
            f"{msg.role if isinstance(msg.role, str) else msg.role.value}: {msg.content}" 
            for msg in chat_history[-10:]
        ])
        
        # Tool-specific extraction
        if tool_type == ToolType.NOTE_MAKER:
            return await self._extract_note_maker_params(
                message, history_text, user_info
            )
        elif tool_type == ToolType.FLASHCARD_GENERATOR:
            return await self._extract_flashcard_params(
                message, history_text, user_info
            )
        else:  # CONCEPT_EXPLAINER
            return await self._extract_concept_explainer_params(
                message, history_text, user_info
            )
    
    async def _extract_note_maker_params(
        self,
        message: str,
        history: str,
        user_info: UserInfo
    ) -> ExtractedParameters:
        """Extract parameters for Note Maker tool."""
        
        prompt = f"""You are an expert parameter extractor. Extract parameters for a note-making tool.

Student Profile:
- Grade: {user_info.grade_level}
- Mastery: {user_info.mastery_level_summary}
- Learning Style: {user_info.learning_style_summary}
- Emotional State: {user_info.emotional_state_summary}

Conversation History:
{history}

Current Message: "{message}"

Required Parameters:
1. topic - The main topic for notes (extract from message or history)
2. subject - Academic subject (e.g., Biology, Math, History)
3. note_taking_style - Choose from: outline, bullet_points, narrative, structured

Optional Parameters:
4. include_examples - true/false (default: true)
5. include_analogies - true/false (default: false unless "visual" learner or "confused")

Inference Rules:
- If learning style mentions "visual" or "imagery" → include_analogies: true
- If emotional state is "confused" or "anxious" → note_taking_style: "bullet_points" (simpler)
- If mastery level is low (1-3) → include_examples: true, include_analogies: true
- If grade level < 8 → simpler style
- If not specified, infer subject from topic (e.g., "photosynthesis" → "Biology")

Return a JSON object with:
{{
    "topic": "extracted topic",
    "subject": "extracted subject",
    "note_taking_style": "one of the 4 options",
    "include_examples": true/false,
    "include_analogies": true/false,
    "inferred": ["list", "of", "inferred", "parameters"],
    "missing": ["list", "of", "missing", "required", "parameters"],
    "confidence": 0.0-1.0
}}

Return ONLY valid JSON, no explanation.
"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            result = json.loads(clean_json_response(response.content))
            
            # Build ExtractedParameters
            inferred_params = {
                param: str(result.get(param, "N/A")) 
                for param in result.get("inferred", [])
            }
            
            # Clean parameters dict - remove metadata fields
            clean_params = {
                k: v for k, v in result.items()
                if k not in ["inferred", "missing", "confidence"]
            }
            
            return ExtractedParameters(
                tool_type=ToolType.NOTE_MAKER,
                parameters=clean_params,
                confidence=result.get("confidence", 0.8),
                missing_required=result.get("missing", []),
                inferred_params=inferred_params
            )
            
        except Exception as e:
            logger.error(f"Error extracting note maker params: {e}")
            # Fallback extraction
            return ExtractedParameters(
                tool_type=ToolType.NOTE_MAKER,
                parameters={
                    "topic": "general study topic",
                    "subject": "General",
                    "note_taking_style": "bullet_points",
                    "include_examples": True,
                    "include_analogies": False
                },
                confidence=0.3,
                missing_required=["topic", "subject"],
                inferred_params={}
            )
    
    async def _extract_flashcard_params(
        self,
        message: str,
        history: str,
        user_info: UserInfo
    ) -> ExtractedParameters:
        """Extract parameters for Flashcard Generator tool."""
        
        prompt = f"""You are an expert parameter extractor. Extract parameters for a flashcard generator.

Student Profile:
- Grade: {user_info.grade_level}
- Mastery: {user_info.mastery_level_summary}
- Emotional State: {user_info.emotional_state_summary}

Conversation History:
{history}

Current Message: "{message}"

Required Parameters:
1. topic - Topic for flashcards
2. count - Number of flashcards (1-20)
3. difficulty - One of: easy, medium, hard
4. subject - Academic subject

Optional Parameters:
5. include_examples - true/false (default: true)

Inference Rules:
- "struggling", "confused", "don't understand" → difficulty: easy
- "confident", "challenge me", "ready" → difficulty: hard
- Default → difficulty: medium
- "few", "quick", "some" → count: 5
- "many", "lots", "thorough" → count: 15
- Default count: 5
- If mastery level 1-3 → difficulty: easy
- If mastery level 4-6 → difficulty: medium
- If mastery level 7-10 → difficulty: medium or hard (based on message tone)
- If emotional state "anxious" or "confused" → reduce difficulty by one level

Return a JSON object with:
{{
    "topic": "extracted topic",
    "count": 5,
    "difficulty": "easy/medium/hard",
    "subject": "extracted subject",
    "include_examples": true/false,
    "inferred": ["list", "of", "inferred", "parameters"],
    "missing": ["list", "of", "missing", "required", "parameters"],
    "confidence": 0.0-1.0
}}

Return ONLY valid JSON, no explanation.
"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            result = json.loads(clean_json_response(response.content))
            
            # Validate count
            count = result.get("count", 5)
            if not isinstance(count, int) or count < 1 or count > 20:
                result["count"] = 5
            
            inferred_params = {
                param: str(result.get(param, "N/A")) 
                for param in result.get("inferred", [])
            }
            
            # Clean parameters dict - remove metadata fields
            clean_params = {
                k: v for k, v in result.items()
                if k not in ["inferred", "missing", "confidence"]
            }
            
            return ExtractedParameters(
                tool_type=ToolType.FLASHCARD_GENERATOR,
                parameters=clean_params,
                confidence=result.get("confidence", 0.8),
                missing_required=result.get("missing", []),
                inferred_params=inferred_params
            )
            
        except Exception as e:
            logger.error(f"Error extracting flashcard params: {e}")
            return ExtractedParameters(
                tool_type=ToolType.FLASHCARD_GENERATOR,
                parameters={
                    "topic": "general topic",
                    "count": 5,
                    "difficulty": "medium",
                    "subject": "General",
                    "include_examples": True
                },
                confidence=0.3,
                missing_required=["topic", "subject"],
                inferred_params={}
            )
    
    async def _extract_concept_explainer_params(
        self,
        message: str,
        history: str,
        user_info: UserInfo
    ) -> ExtractedParameters:
        """Extract parameters for Concept Explainer tool."""
        
        prompt = f"""You are an expert parameter extractor. Extract parameters for a concept explanation tool.

Student Profile:
- Grade: {user_info.grade_level}
- Mastery: {user_info.mastery_level_summary}
- Emotional State: {user_info.emotional_state_summary}

Conversation History:
{history}

Current Message: "{message}"

Required Parameters:
1. concept_to_explain - The specific concept to explain
2. current_topic - Broader topic/subject context
3. desired_depth - One of: basic, intermediate, advanced, comprehensive

Inference Rules:
- If mastery level 1-3 → desired_depth: basic
- If mastery level 4-6 → desired_depth: intermediate
- If mastery level 7-9 → desired_depth: advanced
- If mastery level 10 → desired_depth: comprehensive
- If emotional state "confused" or "anxious" → reduce depth by one level
- If emotional state "focused" or "motivated" → increase depth by one level
- Extract concept from question words: "what is X" → concept: X
- Infer current_topic from subject context in history or from concept itself

Return a JSON object with:
{{
    "concept_to_explain": "extracted concept",
    "current_topic": "broader subject",
    "desired_depth": "basic/intermediate/advanced/comprehensive",
    "inferred": ["list", "of", "inferred", "parameters"],
    "missing": ["list", "of", "missing", "required", "parameters"],
    "confidence": 0.0-1.0
}}

Return ONLY valid JSON, no explanation.
"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            result = json.loads(clean_json_response(response.content))
            
            inferred_params = {
                param: str(result.get(param, "N/A")) 
                for param in result.get("inferred", [])
            }
            
            # Clean parameters dict - remove metadata fields
            clean_params = {
                k: v for k, v in result.items()
                if k not in ["inferred", "missing", "confidence"]
            }
            
            return ExtractedParameters(
                tool_type=ToolType.CONCEPT_EXPLAINER,
                parameters=clean_params,
                confidence=result.get("confidence", 0.8),
                missing_required=result.get("missing", []),
                inferred_params=inferred_params
            )
            
        except Exception as e:
            logger.error(f"Error extracting concept explainer params: {e}")
            return ExtractedParameters(
                tool_type=ToolType.CONCEPT_EXPLAINER,
                parameters={
                    "concept_to_explain": "general concept",
                    "current_topic": "General",
                    "desired_depth": "intermediate"
                },
                confidence=0.3,
                missing_required=["concept_to_explain", "current_topic"],
                inferred_params={}
            )
    
    async def generate_clarification_question(
        self,
        missing_params: List[str],
        tool_type: ToolType,
        context: str
    ) -> str:
        """
        Generate a natural clarification question when required parameters are missing.
        
        Args:
            missing_params: List of missing parameter names
            tool_type: Which tool we're asking for
            context: User's original message
            
        Returns:
            Natural clarification question
        """
        # Handle both ToolType enum and string
        if isinstance(tool_type, str):
            tool_type = ToolType(tool_type)
            
        param_str = ", ".join(missing_params)
        
        prompt = f"""Generate a natural, friendly clarification question.

Tool Type: {tool_type.value}
Missing Parameters: {param_str}
User's Message: "{context}"

Generate a single, natural question that asks for the missing information without being technical.
Don't mention "parameters" or technical terms. Be conversational and helpful.

Examples:
- Missing "topic" → "What topic would you like me to create notes about?"
- Missing "count", "difficulty" → "How many flashcards would you like, and what difficulty level?"
- Missing "concept" → "Which concept would you like me to explain?"

Return ONLY the question, no explanation.
"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            return response.content.strip()
        except Exception as e:
            logger.error(f"Error generating clarification: {e}")
            # Simple fallback
            if "topic" in missing_params:
                return "What topic would you like to learn about?"
            elif "concept_to_explain" in missing_params:
                return "Which concept would you like me to explain?"
            else:
                return f"Could you provide more details about {missing_params[0]}?"


# Global service instance
gemini_service = GeminiService()
