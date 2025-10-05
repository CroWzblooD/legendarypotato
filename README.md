# 🎓 AI Tutor Orchestrator

> **Intelligent Middleware for Autonomous Educational Tool Orchestration**

An advanced AI-powered orchestration system that intelligently routes student requests to the most appropriate educational tools using Google Gemini AI, LangGraph workflows, and PostgreSQL persistence.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00A67E?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0.65-1C3A56?style=flat)](https://github.com/langchain-ai/langgraph)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat&logo=postgresql)](https://postgresql.org)
[![Google Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-4285F4?style=flat&logo=google)](https://ai.google.dev/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Demo Script](#-demo-script)
- [Troubleshooting](#-troubleshooting)

---

## 🌟 Overview

The **AI Tutor Orchestrator** is an intelligent middleware system designed for educational technology platforms. It uses advanced AI to:

1. **Understand** student intent from natural language requests
2. **Extract** required parameters automatically
3. **Infer** missing information using context and user profiles
4. **Validate** all inputs against tool schemas
5. **Execute** the appropriate educational tool
6. **Persist** all interactions to PostgreSQL for analytics

### 🎯 Problem Solved

Traditional educational platforms require students to manually navigate through different tools and fill out forms. This orchestrator:

- ✅ Eliminates manual tool selection
- ✅ Automatically infers missing parameters
- ✅ Provides intelligent context-aware assistance
- ✅ Tracks all interactions for improvement
- ✅ Adapts to student learning profiles

---

## ⚡ Key Features

### 🤖 AI-Powered Intent Classification
- Uses **Google Gemini 1.5 Flash** for natural language understanding
- Classifies student requests into tool categories with 90-100% confidence
- Supports: Note Maker, Flashcard Generator, Concept Explainer

### 🔍 Smart Parameter Extraction
- Automatically extracts parameters from conversational text
- **Infers missing parameters** using:
  - User profile (grade level, learning style)
  - Conversation history
  - Contextual clues
- Provides reasoning for each inference

### ✅ Robust Validation
- Pydantic schema validation for all tool inputs
- Detects missing required parameters
- Generates natural language clarification questions

### 🗄️ Complete PostgreSQL Integration
- **5 tables** tracking all operations
- Hosted on **Supabase** for scalability
- Full analytics on parameter inference accuracy

### 📊 Educational Logging System
- **Color-coded terminal output** for workflow visualization
- Shows intent classification, parameter extraction reasoning, and tool execution metrics
- Perfect for demonstrations and debugging

### 🔄 LangGraph Workflow
- **5-node state machine** orchestration
- Handles complex branching logic
- Maintains state across async operations

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                       Student                             │
└─────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────┐
│           FastAPI Orchestrator (Port 8000)               │
│  ┌────────────────────────────────────────────────┐     │
│  │          LangGraph Workflow (5 Nodes)          │     │
│  │  1. Intent Classification (Gemini AI)          │     │
│  │  2. Parameter Extraction (Gemini AI)           │     │
│  │  3. Parameter Validation (Pydantic)            │     │
│  │  4. Tool Execution / Clarification             │     │
│  │  5. Response Generation                        │     │
│  └────────────────────────────────────────────────┘     │
└─────────────────────┬────────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
  ┌──────────┐  ┌─────────┐  ┌──────────┐
  │ Gemini   │  │ Tools   │  │PostgreSQL│
  │ 1.5Flash │  │ Service │  │(Supabase)│
  │          │  │Port 8001│  │5 Tables  │
  └──────────┘  └─────────┘  └──────────┘
```

---

## 📁 Project Structure

```
backend/
├── 📁 agents/                    # AI Agent modules
│   ├── tool_executor.py          # Tool execution logic
│   └── validator.py              # Parameter validation
│
├── 📁 api/                       # FastAPI routes
│   └── routes.py                 # Main API endpoints
│
├── 📁 config/                    # Configuration
│   └── settings.py               # Environment settings
│
├── 📁 database/                  # Database layer
│   ├── database.py               # Connection management
│   ├── models.py                 # SQLAlchemy models (5 tables)
│   └── 📁 repositories/          # Data access layer
│
├── 📁 graph/                     # LangGraph workflow
│   └── workflow.py               # 5-node orchestration
│
├── 📁 models/                    # Pydantic schemas
│   └── schemas.py                # Request/response models
│
├── 📁 services/                  # External services
│   └── gemini_service.py         # Gemini AI client
│
├── 📁 utils/                     # Utilities
│   └── educational_logger.py     # Color-coded logging
│
├── 📁 scripts/                   # Utility scripts
│   ├── demo.py                   # Interactive demo ⭐
│   ├── init_db.py                # Database setup
│   └── run_tools_service.py      # Educational tools
│
├── main.py                       # FastAPI entry point
├── requirements.txt              # Dependencies
├── .env.example                  # Config template
└── README.md                     # This file!
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **PostgreSQL** or **Supabase Account** (free)
- **Google API Key** for Gemini AI

### Installation (5 Minutes)

```bash
# 1. Clone repository
git clone <repo-url>
cd legendarypotato/backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup configuration
cp .env.example .env
# Edit .env with your credentials:
#   - GOOGLE_API_KEY (from https://ai.google.dev/)
#   - DATABASE_URL (from Supabase or local PostgreSQL)

# 5. Initialize database
python scripts/init_db.py

# 6. Run the system (3 terminals)
# Terminal 1: Tools Service
python scripts/run_tools_service.py

# Terminal 2: Orchestrator
python main.py

# Terminal 3: Interactive Demo
python scripts/demo.py
```

---

## ⚙️ Configuration

### Required Environment Variables

Edit `.env` file:

```ini
# Google Gemini AI (REQUIRED)
GOOGLE_API_KEY=your_api_key_here

# PostgreSQL Database (REQUIRED)
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# Optional: Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_key
SUPABASE_SERVICE_KEY=your_key

# Application Settings
APP_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
```

### Get Your Credentials

1. **Google Gemini API Key**: [https://ai.google.dev/](https://ai.google.dev/)
2. **Supabase Database**: [https://supabase.com](https://supabase.com) (free tier available)

---

## 🚀 Running the Application

### Step 1: Start Tools Service (Port 8001)

```bash
python scripts/run_tools_service.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

### Step 2: Start Orchestrator (Port 8000)

```bash
python main.py
```

Expected output:
```
INFO:     Starting AI Tutor Orchestrator...
INFO:     ✅ Database connection successful!
INFO:     ✅ Database initialized!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Run Interactive Demo

```bash
python scripts/demo.py
```

You'll see a beautiful terminal interface:
```
╔════════════════════════════════════════════════════════╗
║          🎓 AI TUTOR ORCHESTRATOR DEMO 🎓             ║
║     Intelligent Educational Tool Orchestration        ║
╚════════════════════════════════════════════════════════╝

Your message: I need help with calculus derivatives

🔄 Processing Pipeline:
   ├─ Analyzing intent...
   ├─ Extracting parameters...
   ├─ Validating inputs...
   └─ Executing workflow...

✅ Generated 5 flashcards on calculus derivatives!
```

### Verify Services

- Tools API: [http://localhost:8001/docs](http://localhost:8001/docs)
- Orchestrator API: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 API Documentation

### POST `/api/orchestrate`

Main orchestration endpoint - send a student request and get intelligent tool execution.

**Request:**
```json
{
  "message": "I need practice problems on derivatives",
  "user_info": {
    "user_id": "student-123",
    "name": "John Doe",
    "grade_level": "college",
    "learning_style_summary": "Visual learner",
    "emotional_state_summary": "Ready to learn",
    "mastery_level_summary": "Intermediate",
    "teaching_style": "visual"
  },
  "chat_history": [],
  "conversation_id": "conv-abc123"
}
```

**Response:**
```json
{
  "intent": "flashcard_generator",
  "confidence": 95,
  "extracted_params": {
    "topic": "derivatives",
    "count": 5,
    "difficulty": "medium"
  },
  "tool_response": {
    "flashcards": [...]
  },
  "execution_time_ms": 2500
}
```

**Interactive API Docs**: Visit [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🗄️ Database Schema

### Tables Overview

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `users` | Student profiles | name, grade_level, learning_style |
| `conversations` | Chat sessions | user_id, started_at, message_count |
| `chat_messages` | Message history | conversation_id, role, content |
| `parameter_extractions` | Inference analytics | extracted_params, inferred_params, confidence |
| `tool_executions` | Tool usage logs | tool_type, execution_time_ms, success |

### Query Examples

```sql
-- Get user's conversation history
SELECT * FROM chat_messages 
WHERE conversation_id = 'conv-id' 
ORDER BY created_at;

-- Analyze parameter inference accuracy
SELECT tool_type, AVG(confidence_score) as avg_confidence
FROM parameter_extractions
GROUP BY tool_type;

-- Check tool performance
SELECT tool_type, AVG(execution_time_ms) as avg_time
FROM tool_executions
GROUP BY tool_type;
```

---

## 🎬 Demo Script

The interactive demo (`scripts/demo.py`) provides a complete demonstration.

### Features

- ✨ Beautiful terminal UI with colors
- 👤 User profile setup
- 💬 Interactive conversation loop
- 📊 Real-time processing indicators
- 🗄️ Database persistence visualization
- 📈 Session statistics

### Example Interactions

```
Your message: I'm struggling with calculus derivatives

→ Workflow:
  ✅ Intent: flashcard_generator (95% confidence)
  ✅ Extracted: topic, subject
  ✅ Inferred: difficulty=easy (user said "struggling"), count=5
  ✅ Generated 5 flashcards in 2.5s

Your message: explain the chain rule in detail

→ Workflow:
  ✅ Intent: concept_explainer (98% confidence)
  ✅ Extracted: concept="chain rule", desired_depth="detailed"
  ✅ Generated comprehensive explanation in 3.1s
```

### Demo Commands

- `demo` - Show example questions
- `stats` - Display session statistics
- `quit` / `exit` - End session

---

## 🐛 Troubleshooting

### Database Connection Failed

**Solution**: Check `DATABASE_URL` in `.env` is correct

```bash
# Test connection
python scripts/init_db.py
```

### Gemini API Key Invalid

**Solution**: Verify key in `.env` has no spaces

1. Get fresh key from [https://ai.google.dev/](https://ai.google.dev/)
2. Update `.env`: `GOOGLE_API_KEY=your_key_here`

### Tools Service Not Responding

**Solution**: Ensure tools service is running

```bash
# Check if service is up
curl http://localhost:8001/health
```

### Import Errors

**Solution**: Clear cache and reinstall

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

**Solution**: Change port or kill existing process

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

---

## 📊 Performance Benchmarks

| Operation | Average Time |
|-----------|--------------|
| Intent Classification | 800-1200ms |
| Parameter Extraction | 1000-1500ms |
| Flashcard Generation | 2000-3000ms |
| Note Generation | 4000-6000ms |
| End-to-End Request | 4-8 seconds |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language understanding
- **LangChain/LangGraph** for workflow orchestration
- **FastAPI** for modern async web framework
- **Supabase** for PostgreSQL hosting

---

## 📧 Support

For issues and questions:
- **GitHub Issues**: Create an issue
- **Documentation**: Visit `/docs` endpoint

---

**Built with ❤️ for educational technology**

*Last updated: October 2025*
