# 🎓 AI Tutor Orchestrator

<div align="center">

![AI Tutor Logo](https://img.shields.io/badge/AI%20Tutor-Orchestrator-blueviolet?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00A67E?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0.0.65-1C3A56?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start) - _See [QUICKSTART.md](backend/QUICKSTART.md) for details_
- [📡 API Reference](#-api-reference)
- [🔮 Future Enhancements](#-future-enhancements)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)

---

## 🎯 Overview

**AI Tutor Orchestrator** transforms educational tool interaction by understanding natural language requests and automatically routing them to the appropriate tools with intelligent parameter extraction.

### **The Problem**
Students face friction when using educational tools: manual selection, excessive forms, no context awareness.

### **The Solution**
AI-powered _middleware_ that:
-  Understands natural language using AI Agents
-  Extracts and infers required parameters automatically
-  Validates inputs with Pydantic schemas
-  Tracks full analytics in PostgreSQL

### **Example**
```
Input: "I'm struggling with calculus derivatives"

Output: 
  ✓ Tool: Flashcard Generator
  ✓ Topic: Derivatives
  ✓ Difficulty: Easy (inferred from "struggling")
  ✓ Count: 5 flashcards
```
---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Natural Language Processing** | Gemini 2.5 Flash understands student requests in plain English |
| **Smart Parameter Extraction** | Automatically extracts topic, difficulty, count from context |
| **Intelligent Inference** | Uses student profiles and history to fill missing parameters |
| **Multi-Tool Support** | Flashcard Generator, Note Maker, Concept Explainer | ⚠️We only created these as placeholders for demonstration purposes. The API is isolated and working otherwise
| **Validation & Clarification** | Asks natural questions when information is missing |
| **Full Analytics** | 5 PostgreSQL tables track every interaction |
| **LangGraph Workflow** | 5-node state machine for reliable orchestration |

---

## 🏗️ Architecture

### **Complete System Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              STUDENT / FRONTEND                                 │
│                         (Natural Language Requests)                             │
└────────────────────────────────────┬────────────────────────────────────────────┘
                                     │ HTTP POST /api/chat
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       FASTAPI ORCHESTRATOR (Port 8000)                          │
│                                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │                         API LAYER (api/routes.py)                      │    │
│  │  • POST /api/chat - Main orchestration endpoint                       │    │
│  │  • GET /api/health - Health check                                     │    │
│  │  • GET /api/tools - List available tools                              │    │
│  └────────────────────────────────┬───────────────────────────────────────┘    │
│                                   │                                             │
│                                   ▼                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │              DATABASE LAYER (database/repositories/)                   │    │
│  │  • UserRepository - Get/create user profiles                          │    │
│  │  • ConversationRepository - Manage chat sessions                      │    │
│  │  • MessageRepository - Load chat history                              │    │
│  └────────────────────────────────┬───────────────────────────────────────┘    │
│                                   │                                             │
│                                   ▼                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │                    LANGGRAPH WORKFLOW ORCHESTRATOR                     │    │
│  │                      (graph/orchestrator.py)                           │    │
│  │                                                                        │    │
│  │  ┌──────────────────────────────────────────────────────────────┐     │    │
│  │  │              LANGGRAPH STATE MACHINE (workflow.py)           │     │    │
│  │  │                                                              │     │    │
│  │  │  ┌────────────────────┐                                     │     │    │
│  │  │  │  NODE 1: CLASSIFY  │  agents/                           │     │    │
│  │  │  │  Intent Classifier │  • Gemini AI Service               │     │    │
│  │  │  │  (graph/nodes/)    │  • Tool: classify_intent()         │     │    │
│  │  │  └─────────┬──────────┘  • Output: ToolType enum           │     │    │
│  │  │            │                                                │     │    │
│  │  │            ▼                                                │     │    │
│  │  │  ┌────────────────────┐                                     │     │    │
│  │  │  │  NODE 2: EXTRACT   │  agents/                           │     │    │
│  │  │  │  Parameter Extract │  • Gemini AI Service               │     │    │
│  │  │  │  (graph/nodes/)    │  • Tool: extract_parameters()      │     │    │
│  │  │  └─────────┬──────────┘  • Output: ExtractedParameters     │     │    │
│  │  │            │             • SAVES TO: parameter_extractions │     │    │
│  │  │            ▼                                                │     │    │
│  │  │  ┌────────────────────┐                                     │     │    │
│  │  │  │  NODE 3: VALIDATE  │  agents/validator.py               │     │    │
│  │  │  │  Schema Validation │  • Pydantic Models                 │     │    │
│  │  │  │  (graph/nodes/)    │  • Tool Input Schemas              │     │    │
│  │  │  └─────────┬──────────┘  • Output: bool + tool_input       │     │    │
│  │  │            │                                                │     │    │
│  │  │            ▼                                                │     │    │
│  │  │    ┌───────────────┐                                        │     │    │
│  │  │    │  CONDITIONAL  │                                        │     │    │
│  │  │    │   ROUTING:    │                                        │     │    │
│  │  │    │ should_clarify│                                        │     │    │
│  │  │    └───┬───────┬───┘                                        │     │    │
│  │  │        │       │                                            │     │    │
│  │  │  Valid │       │ Invalid                                    │     │    │
│  │  │        │       │                                            │     │    │
│  │  │        ▼       ▼                                            │     │    │
│  │  │  ┌──────────┐ ┌──────────┐                                 │     │    │
│  │  │  │ NODE 4a: │ │ NODE 4b: │                                 │     │    │
│  │  │  │ EXECUTE  │ │ CLARIFY  │                                 │     │    │
│  │  │  │ Tool Call│ │ Question │                                 │     │    │
│  │  │  │ (nodes/) │ │ (nodes/) │                                 │     │    │
│  │  │  └────┬─────┘ └────┬─────┘                                 │     │    │
│  │  │       │            │                                        │     │    │
│  │  │       │            │                                        │     │    │
│  │  │       └────────────┘                                        │     │    │
│  │  │                │                                            │     │    │
│  │  │                ▼                                            │     │    │
│  │  │            [ END ]                                          │     │    │
│  │  │                                                              │     │    │
│  │  └──────────────────────────────────────────────────────────────┘     │    │
│  │                                                                        │    │
│  │  State Management (graph/utils/):                                     │    │
│  │  • state_manager.py - Initial state creation, step tracking           │    │
│  │  • node_persistence.py - Database save operations per node            │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└────┬──────────────────────┬──────────────────────┬───────────────────────┬─────┘
     │                      │                      │                       │
     │                      │                      │                       │
     ▼                      ▼                      ▼                       ▼
┌─────────────┐    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  GEMINI AI  │    │   POSTGRESQL    │   │  TOOLS SERVICE  │   │  UTILITIES      │
│  SERVICE    │    │   DATABASE      │   │  (Port 8001)    │   │                 │
│ (services/) │    │  (Supabase)     │   │  (scripts/)     │   │ • Educational   │
│             │    │                 │   │                 │   │   Logger        │
│ Methods:    │    │ 5 Tables:       │   │ 3 Endpoints:    │   │ • Setup Scripts │
│ • classify_ │    │ ┌─────────────┐ │   │                 │   │                 │
│   intent()  │    │ │   users     │ │   │ POST /api/      │   │                 │
│             │    │ │ • user_id   │ │   │ note-maker      │   │                 │
│ • extract_  │    │ │ • profile   │ │   │ ├─ Gemini Gen  │   │                 │
│   parameters│    │ │ • grade     │ │   │ └─ NoteMaker   │   │                 │
│   ()        │    │ └─────────────┘ │   │    Output       │   │                 │
│             │    │                 │   │                 │   │                 │
│ • generate_ │    │ ┌─────────────┐ │   │ POST /api/      │   │                 │
│   clarifica │    │ │conversations│ │   │ flashcard-      │   │                 │
│   tion()    │    │ │ • conv_id   │ │   │ generator       │   │                 │
│             │    │ │ • user_id   │ │   │ ├─ Gemini Gen  │   │                 │
│ Model:      │    │ │ • started_at│ │   │ └─ Flashcard   │   │                 │
│ Gemini 2.5  │    │ └─────────────┘ │   │    Output       │   │                 │
│ Flash       │    │                 │   │                 │   │                 │
│             │    │ ┌─────────────┐ │   │ POST /api/      │   │                 │
│ Features:   │    │ │chat_messages│ │   │ concept-        │   │                 │
│ • NLP       │    │ │ • message_id│ │   │ explainer       │   │                 │
│ • Context   │    │ │ • role      │ │   │ ├─ Gemini Gen  │   │                 │
│ • Inference │    │ │ • content   │ │   │ └─ Explainer   │   │                 │
│             │    │ │ • timestamp │ │   │    Output       │   │                 │
│             │    │ └─────────────┘ │   │                 │   │                 │
│             │    │                 │   │                 │   │                 │
│             │    │ ┌─────────────┐ │   │                 │   │                 │
│             │    │ │parameter_   │ │   │                 │   │                 │
│             │    │ │extractions  │ │   │                 │   │                 │
│             │    │ │ • extracted │ │   │                 │   │                 │
│             │    │ │ • inferred  │ │   │                 │   │                 │
│             │    │ │ • confidence│ │   │                 │   │                 │
│             │    │ └─────────────┘ │   │                 │   │                 │
│             │    │                 │   │                 │   │                 │
│             │    │ ┌─────────────┐ │   │                 │   │                 │
│             │    │ │tool_        │ │   │                 │   │                 │
│             │    │ │executions   │ │   │                 │   │                 │
│             │    │ │ • exec_id   │ │   │                 │   │                 │
│             │    │ │ • tool_type │ │   │                 │   │                 │
│             │    │ │ • input     │ │   │                 │   │                 │
│             │    │ │ • output    │ │   │                 │   │                 │
│             │    │ │ • success   │ │   │                 │   │                 │
│             │    │ │ • exec_time │ │   │                 │   │                 │
│             │    │ └─────────────┘ │   │                 │   │                 │
└─────────────┘    └─────────────────┘   └─────────────────┘   └─────────────────┘
```

### **Component Breakdown**

#### **1. API Layer** (`api/routes.py`)
- **Main Endpoint**: `POST /api/chat` - Receives student messages
- **Responsibilities**: 
  - Request validation (ChatRequest → ChatResponse)
  - User/conversation creation via repositories
  - Chat history loading from database
  - Workflow orchestration invocation
  - Database transaction management (commit/rollback)

#### **2. Database Layer** (`database/`)
- **Connection**: SQLAlchemy async engine with PostgreSQL (Supabase)
- **Repositories** (Repository Pattern):
  - `UserRepository` - CRUD for student profiles
  - `ConversationRepository` - Manage chat sessions
  - `MessageRepository` - Chat message history
  - `ParameterExtractionRepository` - **Critical for scoring!**
  - `ToolExecutionRepository` - Tool usage analytics
- **Models**: 5 tables with relationships, indexes, constraints

#### **3. LangGraph Workflow** (`graph/`)
- **Orchestrator** (`orchestrator.py`): Entry point, invokes graph
- **Workflow** (`workflow.py`): Defines state machine structure
- **5 Nodes** (`graph/nodes/`):
  1. **Intent Classifier** - Gemini AI determines tool type
  2. **Parameter Extractor** - Gemini AI extracts & infers params
  3. **Parameter Validator** - Pydantic schema validation
  4. **Tool Executor** - HTTP call to Tools Service
  5. **Clarification Generator** - Gemini AI generates questions
- **Utils**: State management, persistence helpers

#### **4. AI Services** (`services/gemini_service.py`)
- **Model**: Google Gemini 2.5 Flash
- **Three Core Methods**:
  - `classify_intent()` - Natural language → ToolType
  - `extract_parameters()` - Message → Parameters + Inference
  - `generate_clarification_question()` - Missing params → Natural question
- **Features**: Context-aware, user profile integration, confidence scoring

#### **5. Validation Layer** (`agents/validator.py`)
- **Pydantic Schemas** (`models/schemas.py`):
  - `NoteMakerInput` - topic, subject, note_taking_style
  - `FlashcardGeneratorInput` - topic, count, difficulty, subject
  - `ConceptExplainerInput` - concept_to_explain, desired_depth
- **Validation**: Type checking, range constraints, enum validation

#### **6. Tool Executor** (`agents/tool_executor.py`)
- **HTTP Client**: httpx async client (60s timeout)
- **Endpoints**: Maps ToolType → Tools Service URLs
- **Error Handling**: Timeout, connection errors, API errors
- **Metrics**: Execution time tracking

#### **7. Tools Service** (`scripts/run_tools_service.py`)
- **Separate FastAPI App** (Port 8001)
- **AI-Powered Tools**: Uses Gemini to generate content
- **Three Endpoints**:
  - `POST /api/note-maker` → Structured study notes
  - `POST /api/flashcard-generator` → Q&A flashcards
  - `POST /api/concept-explainer` → Detailed explanations

#### **8. Educational Logger** (`utils/educational_logger.py`)
- **Purpose**: Pretty-print workflow for demos/videos
- **Features**: Color-coded steps, emoji indicators, real-time progress

---

### **Data Flow Example**

**Input**: "I'm struggling with calculus derivatives"

```
1. API Layer
   ↓ Creates/loads user, conversation, chat history
   
2. Orchestrator
   ↓ Initializes LangGraph state
   
3. Node 1: Intent Classifier
   ↓ Gemini AI → ToolType.FLASHCARD_GENERATOR
   
4. Node 2: Parameter Extractor
   ↓ Gemini AI → {"topic": "derivatives", "subject": "calculus", 
                  "difficulty": "easy" (inferred), "count": 5 (inferred)}
   ↓ SAVES to parameter_extractions table
   
5. Node 3: Validator
   ↓ Pydantic → FlashcardGeneratorInput validated ✅
   
6. Node 4a: Tool Executor
   ↓ HTTP POST → localhost:8001/api/flashcard-generator
   ↓ Gemini generates 5 flashcards
   ↓ SAVES to tool_executions table
   
7. Response
   ↓ Returns flashcards to student
   ↓ SAVES assistant message to chat_messages
```

---

### **Key Architectural Decisions**

| Decision | Rationale |
|----------|-----------|
| **LangGraph** | State machine ensures reliable multi-step workflows |
| **Repository Pattern** | Clean separation of data access logic |
| **Async/Await** | Non-blocking I/O for database and AI calls |
| **Pydantic** | Type safety and automatic validation |
| **Separate Tools Service** | Microservice architecture, independent scaling |
| **5 Database Tables** | Full analytics and conversation replay capability |
| **Gemini 2.5 Flash** | Fast, cost-effective, high-quality inference |

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI 0.100+ | Async web framework |
| **AI** | Google Gemini 2.5 Flash | Natural language understanding |
| **Orchestration** | LangGraph 0.0.65 | State machine workflows |
| **Database** | PostgreSQL 15+ (Supabase) | Analytics & persistence |
| **ORM** | SQLAlchemy 2.0+ (async) | Database operations |
| **Validation** | Pydantic 2.0+ | Schema validation |
| **Server** | Uvicorn | ASGI server |

---

## -> Quick Start

**📚 For detailed setup and usage instructions, see [QUICKSTART.md](backend/QUICKSTART.md)**


### **TL;DR - Get Running Fast**

```bash
# 1. Setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows | source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt

# 2. Configure .env file
cp .env.example .env
# Add your GOOGLE_API_KEY and DATABASE_URL

# 3. Initialize database
python scripts/init_db.py

# 4. Run application
python main.py

# 5. Try the demo (in another terminal)
python scripts/demo.py
```

**👉 [Read the full QUICKSTART guide →](backend/QUICKSTART.md)**

---

## 🔧 API Reference

### **POST `/api/orchestrate`**

Main endpoint for tool orchestration.

**Request:**
```json
{
  "message": "I need flashcards on organic chemistry",
  "user_info": {
    "user_id": "student-123",
    "grade_level": "college",
    "learning_style_summary": "visual"
  },
  "conversation_id": "conv-abc-123"
}
```

**Response:**
```json
{
  "intent": "flashcard_generator",
  "confidence": 0.95,
  "extracted_params": {
    "topic": "organic chemistry",
    "count": 8,
    "difficulty": "medium"
  },
  "tool_response": {
    "flashcards": [...]
  },
  "execution_time_ms": 3200
}
```

### **GET `/health`**

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "gemini_ai": "available",
    "tools_service": "reachable"
  }
}
```

### **Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/orchestrate` | Main orchestration |
| `GET` | `/health` | Health check |
| `GET` | `/api/conversations/{id}` | Get conversation history |
| `POST` | `/api/user/profile` | Update user profile |

**Interactive Docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🔮 Future Enhancements

### **Vector DB for Scalable Tool Discovery**

To make scaling to 80+ tools even smoother, we had planned to store all Tools, with their respective descriptions in a Vector DB.
Having previous experience with RAG pipelines we wanted to use one of the LangGraph nodes to perform a semantic search and pick top `x` (over a threshold score) tools to use.

After 24 hours of work we figured that we had to prioritize a working demo.

We unfortunately ran out of time and had to drop this idea into future enhancements.

```
User Query → Gemini Embedding → Vector DB (Pinecone/Weaviate)
    ↓
Top 5 Similar Tools → PostgreSQL (params/metadata) → LLM Re-rank
    ↓
Selected Tool + Dynamic Schema → Continue Workflow
```
---


