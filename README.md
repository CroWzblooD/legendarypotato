# 🎓 AI Tutor Orchestrator

<div align="center">

![AI Tutor Logo](https://img.shields.io/badge/AI%20Tutor-Orchestrator-blueviolet?style=for-the-badge&logo=openai)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00A67E?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0.0.65-1C3A56?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

**AI-powered intelligent tool orchestration for education**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [💻 Usage](#-usage)
- [🔧 API Reference](#-api-reference)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)

---

## 🎯 Overview

**AI Tutor Orchestrator** transforms educational tool interaction by understanding natural language requests and automatically routing them to the appropriate tools with intelligent parameter extraction.

### **The Problem**
Students face friction when using educational tools: manual selection, excessive forms, no context awareness.

### **The Solution**
AI-powered middleware that:
- 🤖 Understands natural language using Gemini AI (90-100% accuracy)
- 🧠 Extracts and infers required parameters automatically
- ✅ Validates inputs with Pydantic schemas
- 📊 Tracks full analytics in PostgreSQL

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
| **Natural Language Processing** | Gemini 1.5 Flash understands student requests in plain English |
| **Smart Parameter Extraction** | Automatically extracts topic, difficulty, count from context |
| **Intelligent Inference** | Uses student profiles and history to fill missing parameters |
| **Multi-Tool Support** | Flashcard Generator, Note Maker, Concept Explainer |
| **Validation & Clarification** | Asks natural questions when information is missing |
| **Full Analytics** | 5 PostgreSQL tables track every interaction |
| **LangGraph Workflow** | 5-node state machine for reliable orchestration |

---

## 🏗️ Architecture

```
┌──────────────┐
│   STUDENT    │
│ (Natural Lang)│
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────┐
│   FASTAPI ORCHESTRATOR (Port 8000) │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   LangGraph Workflow        │   │
│  │                             │   │
│  │  1. Classify Intent         │   │
│  │  2. Extract Parameters      │   │
│  │  3. Validate Schema         │   │
│  │  4. Execute / Clarify       │   │
│  │  5. Generate Response       │   │
│  └─────────────────────────────┘   │
└────┬────────────────┬───────────────┘
     │                │
┌────▼─────┐    ┌────▼────────┐
│ Gemini AI│    │ PostgreSQL  │
│  (NLP)   │    │  (Analytics)│
└────┬─────┘    └─────────────┘
     │
┌────▼──────────┐
│ Tools Service │
│  (Port 8001)  │
│               │
│ • Flashcards  │
│ • Notes       │
│ • Explainer   │
└───────────────┘
```

**Data Flow:**
1. Student sends natural language request
2. Gemini classifies intent and extracts parameters
3. Pydantic validates all fields
4. System calls tool API or requests clarification
5. Results saved to database and returned to student

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI 0.100+ | Async web framework |
| **AI** | Google Gemini 1.5 Flash | Natural language understanding |
| **Orchestration** | LangGraph 0.0.65 | State machine workflows |
| **Database** | PostgreSQL 15+ (Supabase) | Analytics & persistence |
| **ORM** | SQLAlchemy 2.0+ (async) | Database operations |
| **Validation** | Pydantic 2.0+ | Schema validation |
| **Server** | Uvicorn | ASGI server |

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.11+
- PostgreSQL 15+ or Supabase account
- Google Gemini API key ([get one here](https://ai.google.dev))

### **Installation**

```bash
# 1. Clone repository
git clone https://github.com/yourusername/legendarypotato.git
cd legendarypotato/backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials:
#   GOOGLE_API_KEY=your_api_key_here
#   DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database

# 5. Initialize database
python scripts/init_db.py

# 6. Verify installation
python scripts/verify_system.py
```

### **Running**

Open 3 terminals:

**Terminal 1 - Tools Service:**
```bash
cd backend
uvicorn scripts.run_tools_service:app --port 8001 --reload
```

**Terminal 2 - Orchestrator:**
```bash
cd backend
uvicorn main:app --port 8000 --reload
```

**Terminal 3 - Interactive Demo:**
```bash
cd backend
python scripts\demo.py
```

**Verify:**
- Tools API: http://localhost:8001/docs
- Orchestrator API: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## 💻 Usage

### **Interactive Demo**

```bash
python scripts\demo.py
```

**Example Session:**
```
Your message: I need help with calculus derivatives

🔍 INTENT CLASSIFICATION
   Tool: flashcard_generator
   Confidence: 95%
   
🧠 PARAMETER EXTRACTION
   ✓ Extracted: topic="derivatives", subject="calculus"
   ✓ Inferred: difficulty="easy", count=5
   💡 Reasoning: User said "need help" suggesting beginner level
   
⚡ EXECUTION (2.5s)
   ✅ Generated 5 flashcards successfully!
```

### **API Usage**

```python
import requests

response = requests.post(
    "http://localhost:8000/api/orchestrate",
    json={
        "message": "Explain photosynthesis in detail",
        "user_info": {
            "user_id": "student-123",
            "name": "Jane",
            "grade_level": "high",
            "learning_style_summary": "visual learner"
        }
    }
)

result = response.json()
print(result["tool_response"])
```

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

## 🐛 Troubleshooting

### **Database Connection Failed**
```bash
# Check DATABASE_URL format in .env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database

# Test connection
python scripts\init_db.py
```

### **Gemini API Key Invalid**
```bash
# Verify key in .env (no quotes)
GOOGLE_API_KEY=AIzaSyC...your_key_here

# Get new key at: https://ai.google.dev/
```

### **Tools Service Not Responding**
```bash
# Check if service is running
netstat -ano | findstr :8001  # Windows
lsof -ti:8001  # Mac/Linux

# Start service
uvicorn scripts.run_tools_service:app --port 8001 --reload
```

### **Port Already in Use**
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID 12345 /F

# Or use different port
uvicorn main:app --port 8080 --reload
```

### **Import Errors**
```bash
# Clear cache
rm -rf **/__pycache__

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Must be 3.11+
```

### **Slow Response Times**
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python main.py

# Check Gemini API rate limits
# Check database connection pool
# Monitor tool service logs
```

**Common Issues:**
- Database URL missing `+asyncpg`
- API key has quotes or spaces
- Virtual environment not activated
- Wrong Python version (< 3.11)
- Port conflicts with other services

---

## 🤝 Contributing

We welcome contributions! Here's how:

### **Quick Start**
```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/legendarypotato.git

# 2. Create branch
git checkout -b feature/amazing-feature

# 3. Make changes
# - Follow existing code style
# - Add type hints and docstrings
# - Write tests if applicable

# 4. Test
python scripts\verify_system.py

# 5. Commit (conventional commits)
git commit -m "feat: add caching for responses"
git commit -m "fix: resolve database timeout"

# 6. Push and create PR
git push origin feature/amazing-feature
```

### **Contribution Types**
- 🐛 Bug fixes
- ✨ New features (tools, caching, etc.)
- 📚 Documentation improvements
- 🧪 Tests
- 🎨 UI/UX enhancements

### **Code Style**
```python
# Use type hints
async def classify_intent(message: str, context: dict) -> dict:
    """Classify user intent using Gemini AI."""
    pass

# Use async/await for I/O
async with database.session() as session:
    result = await session.execute(query)
```

### **Commit Convention**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code formatting
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

</div>
