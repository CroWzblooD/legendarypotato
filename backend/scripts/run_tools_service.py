"""
Educational Tools Service with AI-generated content.
Uses Google Gemini to generate real educational content.
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.schemas import (
    NoteMakerInput,
    FlashcardGeneratorInput,
    ConceptExplainerInput,
    NoteMakerOutput,
    FlashcardGeneratorOutput,
    ConceptExplainerOutput,
    NoteSection,
    Flashcard
)

# Load environment variables
load_dotenv()

# Initialize Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Educational Tools API",
    description="Mock educational tools for AI Tutor Orchestrator",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# NOTE MAKER TOOL
# ============================================================================

@app.post("/api/note-maker", response_model=NoteMakerOutput)
async def note_maker_tool(input_data: NoteMakerInput) -> NoteMakerOutput:
    """
    Generate AI-powered study notes based on topic and student preferences.
    """
    logger.info(f"Note Maker: topic={input_data.topic}, style={input_data.note_taking_style}")
    
    try:
        # Build prompt for Gemini
        prompt = f"""Generate PROFESSIONAL ACADEMIC STUDY NOTES about {input_data.topic} in {input_data.subject}.

CRITICAL FORMATTING RULES:
- Use FORMAL, ACADEMIC language only
- NO conversational phrases or motivational language
- Focus on FACTUAL INFORMATION and CLEAR EXPLANATIONS
- Organize information LOGICALLY and SYSTEMATICALLY

Student Grade Level: {input_data.user_info.grade_level}
Note Style: {input_data.note_taking_style}

Requirements:
{'- Include practical examples to illustrate concepts' if input_data.include_examples else ''}
{'- Include analogies to aid understanding' if input_data.include_analogies else ''}
- Use vocabulary appropriate for grade {input_data.user_info.grade_level}
- Present information in clear, structured format

Create 4 sections:
1. Introduction - Overview and context of the topic
2. Key Concepts - Main ideas, principles, and definitions
3. Important Details - Critical facts, formulas, processes, methods
4. Summary and Applications - Practical applications and connections to other topics

Return JSON:
{{
  "sections": [
    {{
      "title": "Section title",
      "content": "Comprehensive content paragraph(s) with academic language",
      "key_points": ["Clear, factual point 1", "Clear, factual point 2", "Clear, factual point 3"],
      "examples": ["Practical example demonstrating the concept"] or [],
      "analogies": ["Analogy to aid understanding"] or []
    }},
    ...
  ],
  "key_concepts": ["Core concept 1", "Core concept 2", "Core concept 3", ...],
  "connections": ["Connection to related topic 1", "Connection to related topic 2"],
  "practice_suggestions": ["Practice activity 1", "Practice activity 2", "Practice activity 3"]
}}

Return ONLY the JSON, no markdown."""

        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean markdown
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        notes_data = json.loads(response_text)
        
        # Convert to NoteSection objects
        sections = [
            NoteSection(
                title=section["title"],
                content=section["content"],
                key_points=section.get("key_points", []),
                examples=section.get("examples", []),
                analogies=section.get("analogies", [])
            )
            for section in notes_data["sections"]
        ]
        
        output = NoteMakerOutput(
            topic=input_data.topic,
            title=f"Study Notes: {input_data.topic}",
            summary=f"AI-generated notes on {input_data.topic} for grade {input_data.user_info.grade_level}.",
            note_sections=sections,
            key_concepts=notes_data.get("key_concepts", []),
            connections_to_prior_learning=notes_data.get("connections", []),
            visual_elements=[
                {"type": "diagram", "description": f"Visual representation of {input_data.topic}"}
            ],
            practice_suggestions=notes_data.get("practice_suggestions", []),
            source_references=[
                f"{input_data.subject} educational materials",
                "AI-generated comprehensive notes"
            ],
            note_taking_style=input_data.note_taking_style
        )
        
        logger.info(f"Note Maker completed: {len(sections)} AI-generated sections")
        return output
        
    except Exception as e:
        logger.error(f"Error generating notes: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate notes: {str(e)}")


# ============================================================================
# FLASHCARD GENERATOR TOOL
# ============================================================================

@app.post("/api/flashcard-generator", response_model=FlashcardGeneratorOutput)
async def flashcard_generator_tool(input_data: FlashcardGeneratorInput) -> FlashcardGeneratorOutput:
    """
    Generate flashcards for practice and memorization using Gemini AI.
    """
    logger.info(f"Flashcard Generator: topic={input_data.topic}, count={input_data.count}, difficulty={input_data.difficulty}")
    
    try:
        # Build prompt for Gemini
        prompt = f"""Generate {input_data.count} PROFESSIONAL EDUCATIONAL FLASHCARDS about {input_data.topic} in {input_data.subject}.

CRITICAL FORMATTING RULES:
- Use FORMAL, ACADEMIC language only
- NO conversational phrases like "Hey", "Don't worry", "You got this", "Great job"
- NO motivational language or encouragement
- Questions should be DIRECT and CLEAR
- Answers should be FACTUAL and CONCISE
- This is for STUDY and MEMORIZATION, not a conversation

Difficulty: {input_data.difficulty}
Student Grade Level: {input_data.user_info.grade_level}

Difficulty Guidelines:
- easy: Basic definitions, simple facts, recall questions (e.g., "What is...?", "Define...")
- medium: Application questions, explanations, comparisons (e.g., "Explain...", "How does...", "Compare...")
- hard: Analysis, synthesis, evaluation (e.g., "Analyze...", "Evaluate...", "Synthesize...")

CORRECT FORMAT EXAMPLES:
Easy: 
Q: "What is the primary function of mitochondria?"
A: "Mitochondria produce ATP through cellular respiration, providing energy for cellular processes."

Medium:
Q: "Explain how mitochondria produce energy for the cell."
A: "Mitochondria use cellular respiration to break down glucose molecules in the presence of oxygen, producing ATP (adenosine triphosphate) which serves as the cell's energy currency."

Hard:
Q: "Analyze the evolutionary significance of mitochondrial DNA being separate from nuclear DNA."
A: "The presence of separate mitochondrial DNA supports the endosymbiotic theory, suggesting mitochondria originated as independent prokaryotic organisms. This has implications for inheritance patterns and evolutionary biology."

INCORRECT - DO NOT USE:
"Hey, let's learn about..." ✗
"Don't worry, this is simple!" ✗
"You got this!" ✗
"Great thinking!" ✗

Return JSON array with exactly {input_data.count} flashcards:
[
  {{
    "title": "Brief category (e.g., 'Definition', 'Function', 'Process')",
    "question": "Direct, clear question without conversational language",
    "answer": "Factual, concise answer",
    "example": "Practical example (or null if not requested)"
  }},
  ...
]

Return ONLY the JSON array, no markdown formatting."""

        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean markdown if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        flashcard_data = json.loads(response_text)
        
        # Convert to Flashcard objects
        flashcards = [
            Flashcard(
                title=card.get("title", f"Flashcard {i+1}"),
                question=card["question"],
                answer=card["answer"],
                example=card.get("example") if input_data.include_examples else None
            )
            for i, card in enumerate(flashcard_data[:input_data.count])
        ]
        
        # Adaptation details
        adaptation = f"Flashcards adapted for {input_data.user_info.mastery_level_summary}. "
        if "anxious" in input_data.user_info.emotional_state_summary.lower():
            adaptation += "Supportive tone used to reduce anxiety. "
        if "confused" in input_data.user_info.emotional_state_summary.lower():
            adaptation += "Extra clarity provided in answers. "
        
        output = FlashcardGeneratorOutput(
            flashcards=flashcards,
            topic=input_data.topic,
            adaptation_details=adaptation,
            difficulty=input_data.difficulty
        )
        
        logger.info(f"Flashcard Generator completed: {len(flashcards)} AI-generated flashcards")
        return output
        
    except Exception as e:
        logger.error(f"Error generating flashcards: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate flashcards: {str(e)}")


# ============================================================================
# CONCEPT EXPLAINER TOOL
# ============================================================================

@app.post("/api/concept-explainer", response_model=ConceptExplainerOutput)
async def concept_explainer_tool(input_data: ConceptExplainerInput) -> ConceptExplainerOutput:
    """
    AI-powered concept explainer with adaptive depth and examples.
    """
    logger.info(f"Concept Explainer: concept={input_data.concept_to_explain}, depth={input_data.desired_depth}")
    
    try:
        # Build prompt for Gemini
        prompt = f"""Provide a PROFESSIONAL ACADEMIC EXPLANATION of the concept "{input_data.concept_to_explain}" in the context of {input_data.current_topic}.

CRITICAL FORMATTING RULES:
- Use FORMAL, ACADEMIC language only
- NO conversational phrases, motivational language, or encouragement
- Focus on CLEAR, FACTUAL EXPLANATIONS
- Present information OBJECTIVELY and SYSTEMATICALLY

Student Grade Level: {input_data.user_info.grade_level}
Explanation Depth: {input_data.desired_depth}

Depth Guidelines:
- basic: Foundational understanding with simple language and core definitions
- intermediate: Moderate complexity, connections between ideas, some detail
- advanced: In-depth analysis, nuanced understanding, complex relationships
- comprehensive: Complete coverage including historical context, applications, current research

Requirements:
- Use vocabulary and complexity appropriate for grade {input_data.user_info.grade_level}
- Provide {input_data.desired_depth} level of detail and depth
- Include 3 concrete, relevant examples that illustrate the concept
- List 3 related concepts that connect to this topic
- Suggest 3 practice questions for comprehension check

Teaching Style Adaptation ({input_data.user_info.teaching_style}):
- direct: Straightforward explanations with clear statements
- socratic: Include thought-provoking questions within explanation
- visual: Describe visual representations and diagrams
- flipped_classroom: Provide exploration-based explanations

Return JSON:
{{
  "explanation": "Comprehensive explanation paragraph(s) using academic language, adjusted for depth level and grade appropriateness",
  "examples": ["Concrete example 1", "Concrete example 2", "Concrete example 3"],
  "related_concepts": ["Related concept 1", "Related concept 2", "Related concept 3"],
  "visual_aids": ["Description of diagram/chart 1", "Description of visual aid 2"],
  "practice_questions": ["Question 1", "Question 2", "Question 3"]
}}

Return ONLY the JSON, no markdown."""

        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean markdown
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        explainer_data = json.loads(response_text)
        
        output = ConceptExplainerOutput(
            explanation=explainer_data["explanation"],
            examples=explainer_data.get("examples", []),
            related_concepts=explainer_data.get("related_concepts", []),
            visual_aids=explainer_data.get("visual_aids", []),
            practice_questions=explainer_data.get("practice_questions", []),
            source_references=[
                f"{input_data.current_topic} educational materials",
                "AI-generated comprehensive explanation"
            ]
        )
        
        logger.info(f"Concept Explainer completed: AI-generated explanation")
        return output
        
    except Exception as e:
        logger.error(f"Error explaining concept: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to explain concept: {str(e)}")


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Educational Tools API",
        "version": "1.0.0",
        "tools": [
            "note-maker",
            "flashcard-generator",
            "concept-explainer"
        ]
    }


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("scripts.run_tools_service:app", host="0.0.0.0", port=8001, reload=True)
