"""
🎓 AI TUTOR ORCHESTRATOR - INTERACTIVE DEMO
Professional demonstration script with clean UI and database integration

This script provides an interactive demo perfect for video recording:
- Clean, colorful terminal UI
- Real-time processing indicators
- Complete conversation flow
- Database persistence visible
- Tool execution with results display
"""
import logging
import sys
import os

# CRITICAL: Completely disable ALL logging before any imports
logging.basicConfig(
    level=logging.CRITICAL,  # Only show CRITICAL errors
    format='',  # No format
    handlers=[logging.NullHandler()]  # Null handler
)

# Disable all SQLAlchemy loggers completely
for logger_name in ['sqlalchemy', 'sqlalchemy.engine', 'sqlalchemy.pool', 
                     'sqlalchemy.dialects', 'sqlalchemy.orm']:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.CRITICAL)
    logger.disabled = True
    logger.propagate = False

import asyncio
from datetime import datetime
import uuid
import time
from typing import Optional

# Add backend to path (parent of scripts folder)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import async_session_maker, init_db, check_db_connection
from database.repositories import (
    UserRepository,
    ConversationRepository,
    MessageRepository,
    ToolExecutionRepository,
    ParameterExtractionRepository
)
from models.schemas import UserInfo, ChatMessage, TeachingStyle
from graph.workflow import orchestrate


# ============================================================================
# COLORS & FORMATTING
# ============================================================================

class Color:
    """ANSI color codes for beautiful terminal output."""
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Reset
    RESET = '\033[0m'


def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Print beautiful banner."""
    clear_screen()
    print(f"{Color.BOLD}{Color.BRIGHT_CYAN}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║                    🎓 AI TUTOR ORCHESTRATOR DEMO 🎓                       ║")
    print("║                                                                            ║")
    print("║              Intelligent Educational Tool Orchestration                   ║")
    print("║                   with PostgreSQL + Gemini AI                             ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Color.RESET}\n")


def print_section(title: str, emoji: str = "📋"):
    """Print section header."""
    print(f"\n{Color.BOLD}{Color.BRIGHT_BLUE}{'─' * 80}{Color.RESET}")
    print(f"{Color.BOLD}{Color.BRIGHT_CYAN}{emoji} {title}{Color.RESET}")
    print(f"{Color.BOLD}{Color.BRIGHT_BLUE}{'─' * 80}{Color.RESET}\n")


def print_success(message: str):
    """Print success message."""
    print(f"{Color.BRIGHT_GREEN}✅ {message}{Color.RESET}")


def print_info(message: str):
    """Print info message."""
    print(f"{Color.BRIGHT_CYAN}ℹ️  {message}{Color.RESET}")


def print_warning(message: str):
    """Print warning message."""
    print(f"{Color.BRIGHT_YELLOW}⚠️  {message}{Color.RESET}")


def print_error(message: str):
    """Print error message."""
    print(f"{Color.BRIGHT_RED}❌ {message}{Color.RESET}")


def print_user_message(message: str):
    """Print user message."""
    print(f"\n{Color.BOLD}{Color.BRIGHT_YELLOW}👤 You:{Color.RESET}")
    print(f"{Color.YELLOW}{message}{Color.RESET}\n")


def print_assistant_message(message: str):
    """Print assistant message."""
    print(f"\n{Color.BOLD}{Color.BRIGHT_GREEN}🤖 AI Tutor:{Color.RESET}")
    print(f"{Color.GREEN}{message}{Color.RESET}\n")


def print_data(label: str, value: str, indent: int = 3):
    """Print labeled data."""
    spaces = " " * indent
    print(f"{spaces}{Color.DIM}{label}:{Color.RESET} {Color.BRIGHT_WHITE}{value}{Color.RESET}")


def print_tool_output(data: dict):
    """Print tool output in a beautiful format."""
    print(f"\n{Color.BOLD}{Color.BRIGHT_MAGENTA}🔧 Tool Output:{Color.RESET}")
    print(f"{Color.BRIGHT_BLACK}{'─' * 80}{Color.RESET}\n")
    
    # Flashcard Generator
    if "flashcards" in data:
        flashcards = data["flashcards"]
        print(f"{Color.BRIGHT_CYAN}📚 Generated {len(flashcards)} Flashcards:{Color.RESET}\n")
        
        for i, card in enumerate(flashcards, 1):
            # Try multiple field names (question/answer or front/back)
            question = card.get('question') or card.get('front', 'N/A')
            answer = card.get('answer') or card.get('back', 'N/A')
            title = card.get('title', '')
            
            # Show title if available
            if title and title != 'N/A':
                print(f"{Color.BOLD}{Color.YELLOW}Card {i} - {title}:{Color.RESET}")
            else:
                print(f"{Color.BOLD}{Color.YELLOW}Card {i}:{Color.RESET}")
            
            print(f"{Color.CYAN}Q: {Color.WHITE}{question}{Color.RESET}")
            print(f"{Color.GREEN}A: {Color.WHITE}{answer}{Color.RESET}")
            
            # Show example if available
            if 'example' in card and card['example']:
                print(f"{Color.DIM}   💡 Example: {card['example']}{Color.RESET}")
            
            if i < len(flashcards):
                print()
    
    # Concept Explainer
    elif "explanation" in data:
        print(f"{Color.BRIGHT_CYAN}📖 Concept Explanation:{Color.RESET}\n")
        
        if "title" in data:
            print(f"{Color.BOLD}{Color.WHITE}{data['title']}{Color.RESET}\n")
        
        print(f"{Color.WHITE}{data['explanation']}{Color.RESET}\n")
        
        if "examples" in data and data["examples"]:
            print(f"\n{Color.BRIGHT_CYAN}💡 Examples:{Color.RESET}")
            for example in data["examples"]:
                print(f"  • {Color.GREEN}{example}{Color.RESET}")
        
        if "analogies" in data and data["analogies"]:
            print(f"\n{Color.BRIGHT_YELLOW}🔗 Analogies:{Color.RESET}")
            for analogy in data["analogies"]:
                print(f"  • {Color.YELLOW}{analogy}{Color.RESET}")
    
    # Note Maker
    elif "note_sections" in data or "notes" in data:
        print(f"{Color.BRIGHT_CYAN}📝 Study Notes:{Color.RESET}\n")
        
        if "title" in data:
            print(f"{Color.BOLD}{Color.WHITE}{data['title']}{Color.RESET}\n")
        
        if "summary" in data:
            print(f"{Color.BRIGHT_BLACK}{data['summary']}{Color.RESET}\n")
        
        # Display sections
        if "note_sections" in data:
            sections = data["note_sections"]
            for section in sections:
                section_title = section.get("title", "Section")
                content = section.get("content", "")
                
                print(f"\n{Color.BOLD}{Color.CYAN}▸ {section_title}{Color.RESET}")
                print(f"{Color.WHITE}{content}{Color.RESET}")
        
        # Display key points if available
        if "key_points" in data and data["key_points"]:
            print(f"\n{Color.BOLD}{Color.BRIGHT_YELLOW}🔑 Key Points:{Color.RESET}")
            for point in data["key_points"]:
                print(f"  • {Color.YELLOW}{point}{Color.RESET}")
    
    else:
        # Fallback: pretty print the whole data
        import json
        print(f"{Color.WHITE}{json.dumps(data, indent=2)}{Color.RESET}")
    
    print(f"\n{Color.BRIGHT_BLACK}{'─' * 80}{Color.RESET}\n")


def print_processing(message: str = "Processing"):
    """Print processing indicator."""
    print(f"{Color.BRIGHT_MAGENTA}⏳ {message}...{Color.RESET}", end="", flush=True)


def print_done():
    """Print done marker."""
    print(f" {Color.BRIGHT_GREEN}Done!{Color.RESET}")


def print_analytics_box(title: str, data: dict):
    """Print analytics in a box."""
    print(f"\n{Color.BOLD}{Color.BG_BLUE}{Color.WHITE} {title} {Color.RESET}")
    print(f"{Color.BRIGHT_BLACK}┌{'─' * 78}┐{Color.RESET}")
    
    for key, value in data.items():
        key_display = key.replace('_', ' ').title()
        print(f"{Color.BRIGHT_BLACK}│{Color.RESET} {Color.CYAN}{key_display:.<40}{Color.RESET} {Color.BRIGHT_WHITE}{value:>36}{Color.RESET} {Color.BRIGHT_BLACK}│{Color.RESET}")
    
    print(f"{Color.BRIGHT_BLACK}└{'─' * 78}┘{Color.RESET}\n")


# ============================================================================
# PROGRESS INDICATOR
# ============================================================================

class ProgressSpinner:
    """Animated spinner for long-running operations."""
    
    def __init__(self, message: str = "Processing"):
        self.message = message
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.running = False
        self.thread = None
    
    def _spin(self):
        """Spin animation."""
        idx = 0
        while self.running:
            char = self.spinner_chars[idx % len(self.spinner_chars)]
            sys.stdout.write(f"\r{Color.BRIGHT_YELLOW}{char}{Color.RESET} {Color.DIM}{self.message}...{Color.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1
    
    def start(self):
        """Start spinner."""
        self.running = True
        import threading
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()
    
    def stop(self, final_message: str = None):
        """Stop spinner."""
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write("\r" + " " * 80 + "\r")  # Clear line
        if final_message:
            print(final_message)
        sys.stdout.flush()


# ============================================================================
# INTERACTIVE FUNCTIONS
# ============================================================================

async def get_user_input_for_profile():
    """Get user profile information interactively."""
    print_section("User Profile Setup", "👤")
    
    print(f"{Color.BRIGHT_CYAN}Let's set up your learning profile!{Color.RESET}\n")
    
    # Get name
    name = input(f"{Color.WHITE}Your name: {Color.RESET}").strip()
    if not name:
        name = f"Student_{uuid.uuid4().hex[:6]}"  # Generate random name if empty
    
    # Get grade
    print(f"\n{Color.DIM}Grade levels: Elementary, Middle School, High School, College, Adult{Color.RESET}")
    grade = input(f"{Color.WHITE}Your grade level: {Color.RESET}").strip()
    if not grade:
        grade = "High School"
    
    # Get learning style
    print(f"\n{Color.DIM}Learning styles: Visual, Socratic, Direct, Flipped{Color.RESET}")
    learning_style_input = input(f"{Color.WHITE}Your preferred teaching style (or press Enter for Visual): {Color.RESET}").strip()
    if not learning_style_input:
        learning_style_input = "Visual"
    
    # Map to teaching style enum - use valid TeachingStyle values
    learning_style_map = {
        "visual": TeachingStyle.VISUAL,
        "socratic": TeachingStyle.SOCRATIC,
        "direct": TeachingStyle.DIRECT,
        "flipped": TeachingStyle.FLIPPED_CLASSROOM,
    }
    
    # Get first word and lowercase for matching
    style_key = learning_style_input.lower().split()[0]
    teaching_style = learning_style_map.get(style_key, TeachingStyle.VISUAL)  # Default to VISUAL
    
    print()  # Empty line
    
    return UserInfo(
        user_id=str(uuid.uuid4()),
        name=name,
        grade_level=grade,
        learning_style_summary=f"{learning_style_input} learner who prefers personalized instruction",
        emotional_state_summary="Ready to learn and explore new topics",
        mastery_level_summary="Building knowledge across subjects",
        teaching_style=teaching_style
    )

async def setup_demo():
    """Setup demo environment."""
    print_section("System Initialization", "🚀")
    
    # Check database
    print_processing("Connecting to PostgreSQL database")
    if not await check_db_connection():
        print_done()
        print_error("Database connection failed!")
        return False
    print_done()
    print_success("Connected to Supabase PostgreSQL")
    
    # Initialize tables
    print_processing("Initializing database tables")
    await init_db()
    print_done()
    print_success("All 5 tables ready (users, conversations, messages, tool_executions, parameter_extractions)")
    
    return True


async def create_user(db, user_info: UserInfo):
    """Create demo user from provided user info."""
    print_section("Creating User Profile", "✨")
    
    user_repo = UserRepository(db)
    user, created = await user_repo.get_or_create(
        user_id=user_info.user_id,
        name=user_info.name,
        grade_level=user_info.grade_level,
        learning_style_summary=user_info.learning_style_summary,
        emotional_state_summary=user_info.emotional_state_summary,
        mastery_level_summary=user_info.mastery_level_summary,
        teaching_style=user_info.teaching_style if isinstance(user_info.teaching_style, str) else user_info.teaching_style.value
    )
    await db.commit()
    
    print_data("Name", user.name)
    print_data("Grade", user.grade_level)
    print_data("Learning Style", user_info.learning_style_summary.split()[0])
    print_data("Teaching Preference", user.teaching_style.capitalize())
    
    if created:
        print_success("\n✨ New user profile created in database")
    else:
        print_info("\n🔄 Existing user profile loaded from database")
    
    return user_info  # Return UserInfo object


async def start_conversation(db, user_id: str):
    """Start new conversation."""
    conversation_id = str(uuid.uuid4())
    
    conv_repo = ConversationRepository(db)
    conversation = await conv_repo.create(
        conversation_id=conversation_id,
        user_id=user_id
    )
    await db.commit()
    
    print_info(f"📝 New conversation started (ID: {conversation_id[:8]}...)")
    
    return conversation_id


async def process_message(message: str, conversation_id: str, chat_history: list, user_info: UserInfo, db):
    """Process user message through orchestrator."""
    print_user_message(message)
    
    # Show processing with spinner
    print(f"{Color.BRIGHT_MAGENTA}🔄 Processing Pipeline:{Color.RESET}")
    print(f"{Color.DIM}   ├─ Analyzing intent...{Color.RESET}")
    print(f"{Color.DIM}   ├─ Extracting parameters...{Color.RESET}")
    print(f"{Color.DIM}   ├─ Validating inputs...{Color.RESET}")
    print(f"{Color.DIM}   └─ Executing workflow...{Color.RESET}\n")
    
    # Start progress spinner
    spinner = ProgressSpinner("Waiting for Gemini AI")
    spinner.start()
    
    start_time = time.time()
    
    # Run orchestration
    result = await orchestrate(
        user_message=message,
        user_info=user_info,
        chat_history=chat_history,
        conversation_id=conversation_id,
        db_session=db
    )
    
    await db.commit()
    
    duration = time.time() - start_time
    
    # Stop spinner
    spinner.stop()
    
    # Show results
    print(f"{Color.BRIGHT_GREEN}✨ Processing Complete{Color.RESET} {Color.DIM}({duration:.2f}s){Color.RESET}\n")
    
    # Show extraction details
    if result.get("extracted_params"):
        params = result["extracted_params"]
        
        confidence_color = Color.BRIGHT_GREEN if params.confidence >= 0.8 else (Color.BRIGHT_YELLOW if params.confidence >= 0.5 else Color.BRIGHT_RED)
        
        print(f"{Color.BOLD}📊 Analysis Results:{Color.RESET}")
        print_data("Intent", result["intent"].value if result.get("intent") else "Unknown")
        print_data("Confidence", f"{confidence_color}{params.confidence:.0%}{Color.RESET}")
        
        if params.parameters:
            print(f"\n{Color.BRIGHT_CYAN}   📦 Extracted Parameters:{Color.RESET}")
            for key, value in params.parameters.items():
                if value is not None:
                    print(f"{Color.DIM}      • {key}:{Color.RESET} {Color.WHITE}{value}{Color.RESET}")
        
        if params.inferred_params:
            print(f"\n{Color.BRIGHT_YELLOW}   🔮 Inferred (from context):{Color.RESET}")
            for key, value in params.inferred_params.items():
                print(f"{Color.DIM}      • {key}:{Color.RESET} {Color.WHITE}{value}{Color.RESET}")
        
        if params.missing_required:
            print(f"\n{Color.BRIGHT_RED}   ❓ Missing Information:{Color.RESET}")
            for param in params.missing_required:
                print(f"{Color.DIM}      • {param}{Color.RESET}")
    
    # Show assistant response
    if result.get("final_message"):
        print_assistant_message(result["final_message"])
    
    # Show tool output if available
    if result.get("tool_response") and result["tool_response"].success:
        tool_resp = result["tool_response"]
        if tool_resp.data:
            print_tool_output(tool_resp.data)
            
            # Show execution stats
            if tool_resp.execution_time_ms:
                print_data("⚡ Execution Time", f"{tool_resp.execution_time_ms}ms", indent=3)
    
    # Update chat history
    from models.schemas import ChatMessage as ChatMsg
    chat_history.append(ChatMsg(role="user", content=message))
    if result.get("final_message"):
        chat_history.append(ChatMsg(role="assistant", content=result["final_message"]))
    
    return result


async def show_conversation_stats(conversation_id: str, db):
    """Show conversation statistics."""
    print_section("Conversation Statistics", "📊")
    
    msg_repo = MessageRepository(db)
    tool_repo = ToolExecutionRepository(db)
    param_repo = ParameterExtractionRepository(db)
    
    # Get counts
    message_count = await msg_repo.count_by_conversation(conversation_id)
    tools = await tool_repo.get_by_conversation(conversation_id)
    
    # Prepare data
    stats = {
        "Total Messages": message_count,
        "Tools Executed": len(tools),
        "Successful Tools": sum(1 for t in tools if t.success),
        "Database Records Saved": message_count + len(tools) + 1,
    }
    
    if tools:
        avg_time = sum(t.execution_time_ms for t in tools if t.execution_time_ms) / len(tools)
        stats["Avg Tool Execution"] = f"{avg_time:.0f}ms"
    
    print_analytics_box("Session Analytics", stats)


async def show_database_summary(db):
    """Show overall database statistics."""
    print_section("Database Summary", "💾")
    
    from sqlalchemy import select, func
    from database.models import User, Conversation, ChatMessage, ToolExecution, ParameterExtraction
    
    # Get counts
    user_count = await db.scalar(select(func.count()).select_from(User))
    conv_count = await db.scalar(select(func.count()).select_from(Conversation))
    msg_count = await db.scalar(select(func.count()).select_from(ChatMessage))
    tool_count = await db.scalar(select(func.count()).select_from(ToolExecution))
    extraction_count = await db.scalar(select(func.count()).select_from(ParameterExtraction))
    
    # Average confidence
    avg_confidence = await db.scalar(select(func.avg(ParameterExtraction.confidence_score)))
    
    # Success rate
    successful_tools = await db.scalar(
        select(func.count()).select_from(ToolExecution).where(ToolExecution.success == True)
    )
    success_rate = (successful_tools / tool_count * 100) if tool_count > 0 else 0
    
    db_stats = {
        "👤 Total Users": user_count or 0,
        "💬 Total Conversations": conv_count or 0,
        "📝 Total Messages": msg_count or 0,
        "🔧 Total Tool Executions": tool_count or 0,
        "🎯 Parameter Extractions": extraction_count or 0,
        "📈 Avg Confidence": f"{avg_confidence:.0%}" if avg_confidence else "N/A",
        "✅ Tool Success Rate": f"{success_rate:.1f}%",
    }
    
    print_analytics_box("PostgreSQL Database (Supabase)", db_stats)


# ============================================================================
# MAIN DEMO FLOW
# ============================================================================

async def interactive_demo():
    """Run interactive demo."""
    print_banner()
    
    # Setup database
    if not await setup_demo():
        return
    
    input(f"\n{Color.BRIGHT_CYAN}Press Enter to continue...{Color.RESET}\n")
    
    # Get user profile
    user_info = await get_user_input_for_profile()
    
    # Create user in database
    async with async_session_maker() as db:
        user_info = await create_user(db, user_info)
        conversation_id = await start_conversation(db, user_info.user_id)
    
    input(f"\n{Color.BRIGHT_CYAN}Press Enter to start chatting...{Color.RESET}\n")
    
    chat_history = []
    
    # Interactive chat loop
    while True:
        print(f"\n{Color.BRIGHT_BLACK}{'═' * 80}{Color.RESET}")
        print(f"{Color.BOLD}{Color.BRIGHT_CYAN}What would you like to learn today?{Color.RESET}")
        print(f"{Color.DIM}(Type 'demo' for example questions, 'stats' for statistics, or 'quit' to exit){Color.RESET}")
        print(f"{Color.BRIGHT_BLACK}{'─' * 80}{Color.RESET}")
        
        user_input = input(f"{Color.BRIGHT_YELLOW}Your message: {Color.RESET}").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            break
        
        if user_input.lower() == 'demo':
            print(f"\n{Color.BRIGHT_CYAN}📝 Example Questions:{Color.RESET}")
            print(f"{Color.GREEN}  1. Create 8 flashcards on photosynthesis, easy level{Color.RESET}")
            print(f"{Color.GREEN}  2. Explain Newton's laws of motion with examples{Color.RESET}")
            print(f"{Color.GREEN}  3. I need study notes on World War II{Color.RESET}")
            print(f"{Color.GREEN}  4. Help me understand chemical bonding{Color.RESET}")
            continue
        
        if user_input.lower() == 'stats':
            async with async_session_maker() as db:
                await show_conversation_stats(conversation_id, db)
                await show_database_summary(db)
            continue
        
        # Process message
        async with async_session_maker() as db:
            try:
                result = await process_message(user_input, conversation_id, chat_history, user_info, db)
            except Exception as e:
                print_error(f"Error: {str(e)}")
                import traceback
                traceback.print_exc()
    
    # Final summary
    print_section("Session Complete", "🎉")
    
    async with async_session_maker() as db:
        await show_conversation_stats(conversation_id, db)
        await show_database_summary(db)
    
    print(f"\n{Color.BRIGHT_GREEN}✨ All conversation data saved to PostgreSQL database!{Color.RESET}")
    print(f"{Color.BRIGHT_CYAN}🔗 View in Supabase: https://skwxttypekeqxjyixrml.supabase.co{Color.RESET}\n")
    
    print(f"{Color.BOLD}{Color.BRIGHT_MAGENTA}Thank you for using AI Tutor Orchestrator!{Color.RESET}\n")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        asyncio.run(interactive_demo())
    except KeyboardInterrupt:
        print(f"\n\n{Color.BRIGHT_YELLOW}Demo interrupted. Goodbye!{Color.RESET}\n")
    except Exception as e:
        print(f"\n{Color.BRIGHT_RED}Error: {e}{Color.RESET}\n")
        import traceback
        traceback.print_exc()
