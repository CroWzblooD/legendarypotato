"""
Mock Educational Tools Service.
This simulates the 3 educational tools with realistic responses.
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os

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
    Generate study notes based on topic and student preferences.
    """
    logger.info(f"Note Maker: topic={input_data.topic}, style={input_data.note_taking_style}")
    
    # Adapt based on student profile
    depth = "basic" if "Level 1" in input_data.user_info.mastery_level_summary or "Level 2" in input_data.user_info.mastery_level_summary else "detailed"
    
    # Generate sections
    sections = [
        NoteSection(
            title="Introduction",
            content=f"Overview of {input_data.topic} in the context of {input_data.subject}.",
            key_points=[
                f"Core concept: {input_data.topic}",
                f"Subject area: {input_data.subject}",
                "Foundation for advanced topics"
            ],
            examples=[f"Example: Real-world application of {input_data.topic}"] if input_data.include_examples else [],
            analogies=[f"Think of {input_data.topic} like..."] if input_data.include_analogies else []
        ),
        NoteSection(
            title="Key Concepts",
            content=f"Main ideas and principles related to {input_data.topic}.",
            key_points=[
                "Fundamental principle 1",
                "Fundamental principle 2",
                "How concepts interconnect"
            ],
            examples=["Practical example demonstrating the concept"] if input_data.include_examples else [],
            analogies=["Analogy to help understand the concept"] if input_data.include_analogies else []
        ),
        NoteSection(
            title="Important Details",
            content=f"Critical information about {input_data.topic} that students should remember.",
            key_points=[
                "Detail 1: Specific fact or formula",
                "Detail 2: Process or method",
                "Detail 3: Common misconception to avoid"
            ],
            examples=["Step-by-step example"] if input_data.include_examples else [],
            analogies=[] 
        ),
        NoteSection(
            title="Summary and Applications",
            content=f"How {input_data.topic} applies in {input_data.subject} and beyond.",
            key_points=[
                "Practical applications",
                "Connection to other topics",
                "Why this matters"
            ],
            examples=["Real-world application example"] if input_data.include_examples else [],
            analogies=[]
        )
    ]
    
    output = NoteMakerOutput(
        topic=input_data.topic,
        title=f"Study Notes: {input_data.topic}",
        summary=f"Comprehensive notes on {input_data.topic} tailored for {input_data.user_info.grade_level} grade level.",
        note_sections=sections,
        key_concepts=[
            f"Core concept of {input_data.topic}",
            f"Relationship to {input_data.subject}",
            "Practical applications",
            "Foundation for advanced study"
        ],
        connections_to_prior_learning=[
            "Builds on previous knowledge",
            f"Connects to other {input_data.subject} concepts"
        ],
        visual_elements=[
            {"type": "diagram", "description": f"Visual representation of {input_data.topic}"}
        ],
        practice_suggestions=[
            f"Practice problems related to {input_data.topic}",
            "Create your own examples",
            "Teach the concept to someone else"
        ],
        source_references=[
            f"{input_data.subject} textbook chapter",
            "Online educational resources"
        ],
        note_taking_style=input_data.note_taking_style
    )
    
    logger.info(f"Note Maker completed: {len(sections)} sections generated")
    return output


# ============================================================================
# FLASHCARD GENERATOR TOOL
# ============================================================================

@app.post("/api/flashcard-generator", response_model=FlashcardGeneratorOutput)
async def flashcard_generator_tool(input_data: FlashcardGeneratorInput) -> FlashcardGeneratorOutput:
    """
    Generate flashcards for practice and memorization.
    """
    logger.info(f"Flashcard Generator: topic={input_data.topic}, count={input_data.count}, difficulty={input_data.difficulty}")
    
    # Generate flashcards based on difficulty
    flashcards = []
    
    difficulty_templates = {
        "easy": [
            ("Definition", f"What is {input_data.topic}?", f"{input_data.topic} is a fundamental concept in {input_data.subject}."),
            ("Basic Fact", f"What subject does {input_data.topic} belong to?", input_data.subject),
            ("Recognition", f"Can you identify {input_data.topic}?", f"Yes, it relates to {input_data.subject}."),
        ],
        "medium": [
            ("Application", f"How is {input_data.topic} used in {input_data.subject}?", f"{input_data.topic} is applied in various scenarios..."),
            ("Explanation", f"Explain the main principle of {input_data.topic}.", f"The core principle involves..."),
            ("Comparison", f"How does {input_data.topic} relate to other concepts?", f"It connects to..."),
        ],
        "hard": [
            ("Analysis", f"Analyze the implications of {input_data.topic}.", f"Deep analysis reveals..."),
            ("Synthesis", f"How would you apply {input_data.topic} to solve complex problems?", f"Strategic approach involves..."),
            ("Evaluation", f"Evaluate different perspectives on {input_data.topic}.", f"Critical evaluation shows..."),
        ]
    }
    
    templates = difficulty_templates.get(input_data.difficulty, difficulty_templates["medium"])
    
    for i in range(input_data.count):
        template = templates[i % len(templates)]
        flashcard = Flashcard(
            title=f"{template[0]} {i+1}",
            question=template[1],
            answer=template[2],
            example=f"Example: Practical application of this concept" if input_data.include_examples else None
        )
        flashcards.append(flashcard)
    
    # Adaptation details based on student profile
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
    
    logger.info(f"Flashcard Generator completed: {len(flashcards)} flashcards generated")
    return output


# ============================================================================
# CONCEPT EXPLAINER TOOL
# ============================================================================

@app.post("/api/concept-explainer", response_model=ConceptExplainerOutput)
async def concept_explainer_tool(input_data: ConceptExplainerInput) -> ConceptExplainerOutput:
    """
    Explain concepts with appropriate depth and examples.
    """
    logger.info(f"Concept Explainer: concept={input_data.concept_to_explain}, depth={input_data.desired_depth}")
    
    # Adjust explanation based on depth
    depth_content = {
        "basic": f"{input_data.concept_to_explain} is a fundamental concept in {input_data.current_topic}. At a basic level, it refers to...",
        "intermediate": f"{input_data.concept_to_explain} is an important concept in {input_data.current_topic}. It involves understanding how... and why... This concept builds on foundational knowledge and extends to...",
        "advanced": f"{input_data.concept_to_explain} represents a sophisticated aspect of {input_data.current_topic}. Advanced understanding requires analyzing the intricate relationships between... considering edge cases... and synthesizing...",
        "comprehensive": f"{input_data.concept_to_explain} is a multifaceted concept in {input_data.current_topic}. A comprehensive understanding encompasses historical context, theoretical foundations, practical applications, current research, and future implications..."
    }
    
    explanation = depth_content.get(input_data.desired_depth, depth_content["intermediate"])
    
    # Adapt based on teaching style
    if hasattr(input_data.user_info, 'teaching_style'):
        if input_data.user_info.teaching_style == "socratic":
            explanation += "\n\nConsider these questions: What makes this concept important? How would you explain it to someone else?"
        elif input_data.user_info.teaching_style == "visual":
            explanation += "\n\nVisualize this concept as..."
    
    output = ConceptExplainerOutput(
        explanation=explanation,
        examples=[
            f"Example 1: Basic application of {input_data.concept_to_explain}",
            f"Example 2: Intermediate case showing {input_data.concept_to_explain}",
            f"Example 3: Advanced scenario demonstrating {input_data.concept_to_explain}"
        ],
        related_concepts=[
            f"Related concept 1 in {input_data.current_topic}",
            f"Related concept 2 in {input_data.current_topic}",
            "Broader theoretical framework"
        ],
        visual_aids=[
            f"Diagram illustrating {input_data.concept_to_explain}",
            f"Flowchart showing process",
            "Comparison chart"
        ],
        practice_questions=[
            f"What is the main purpose of {input_data.concept_to_explain}?",
            f"How does {input_data.concept_to_explain} apply in real situations?",
            f"Can you think of other examples of {input_data.concept_to_explain}?"
        ],
        source_references=[
            f"{input_data.current_topic} textbook",
            "Academic papers on the subject",
            "Educational videos and tutorials"
        ]
    )
    
    logger.info(f"Concept Explainer completed")
    return output


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
    uvicorn.run("tools_main:app", host="0.0.0.0", port=8001, reload=True)
