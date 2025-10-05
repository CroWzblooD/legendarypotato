# 🎓 AI Tutor Orchestrator - Intelligent Educational Tool Orchestration

<div align="center">

![AI Tutor Logo](https://img.shields.io/badge/AI%20Tutor-Orchestrator-blueviolet?style=for-the-badge&logo=openai)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00A67E?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0.0.65-1C3A56?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

**Revolutionizing education through AI-powered intelligent tool orchestration**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

</div>

---

## 📋 Table of Contents

- [🎯 Problem Statement](#-problem-statement)
- [💡 Solution Overview](#-solution-overview)
- [🚀 Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [📦 Installation & Setup](#-installation--setup)
- [🎮 Usage Guide](#-usage-guide)
- [🔬 Technical Details](#-technical-details)
- [📊 Performance Benchmarks](#-performance-benchmarks)
- [🔧 API Documentation](#-api-documentation)
- [🗄️ Database Schema](#️-database-schema)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## � Problem Statement

Traditional educational platforms face **critical usability challenges**:

- **🔧 Manual Tool Selection**: Students must navigate complex interfaces to find the right tool
- **📝 Form Fatigue**: Excessive form-filling reduces learning momentum
- **🤔 Context Loss**: Systems don't remember student preferences or history
- **⚠️ Poor Guidance**: No intelligent suggestions or parameter inference
- **📊 No Analytics**: Limited insight into how tools are actually used

**Key Challenges:**
- Understanding natural language student requests
- Extracting structured parameters from conversational text
- Inferring missing information intelligently
- Validating inputs against tool requirements
- Maintaining context across interactions

---

## 💡 Solution Overview

**AI Tutor Orchestrator** is an **intelligent middleware system** that eliminates friction between students and educational tools through **AI-powered orchestration**.

### 🎯 Core Capabilities

1. **🤖 Intent Recognition**: Gemini AI understands what students need from natural language
2. **🧠 Smart Parameter Extraction**: Automatically extracts required tool parameters
3. **🔮 Intelligent Inference**: Fills missing information using student profiles and context
4. **✅ Robust Validation**: Ensures all inputs meet tool requirements
5. **📈 Full Analytics**: Tracks every interaction for continuous improvement

### 💫 The Magic

```
Student: "I'm struggling with calculus derivatives and need practice"

Traditional System:          AI Tutor Orchestrator:
┌─────────────────┐         ┌─────────────────┐
│ 1. Select Tool  │         │ 1. Understands  │
│ 2. Choose Topic │   VS    │    - Tool: Flashcard Generator
│ 3. Set Count    │         │    - Topic: Derivatives (calculus)
│ 4. Pick Difficulty│       │    - Difficulty: Easy ("struggling")
│ 5. Submit Form  │         │    - Count: 5 (default)
└─────────────────┘         │ 2. Generates instantly! ✨
                            └─────────────────┘
```

---

## 🚀 Key Features

### 🤖 **AI-Powered Intent Classification**

| Feature | Description |
|---------|-------------|
| **Natural Language** | Understands requests in plain English |
| **High Accuracy** | 90-100% confidence scores using Gemini 1.5 Flash |
| **Multi-Tool** | Supports Note Maker, Flashcard Generator, Concept Explainer |
| **Contextual** | Considers conversation history and user profiles |

### 🔍 **Smart Parameter Extraction & Inference**

```python
Input: "I need help with organic chemistry for my exam tomorrow"

Extracted:
  ✓ subject: "organic chemistry"
  ✓ topic: "organic chemistry" 
  ✓ urgency: "tomorrow"

Inferred (from context):
  ✓ difficulty: "medium" (user grade level: college)
  ✓ count: 10 (exam preparation needs more cards)
  ✓ learning_style: "visual" (user profile)
  ✓ format: "detailed" (exam context)

Reasoning:
  💡 "Exam context suggests higher card count for comprehensive review"
  💡 "College level indicates medium difficulty appropriate"
```

### ✅ **Robust Validation System**

- **🔒 Schema Validation**: Pydantic models ensure type safety
- **🔍 Missing Parameter Detection**: Identifies what's needed
- **💬 Natural Clarifications**: Generates human-friendly questions
- **🔄 Interactive Loop**: Continues conversation until all parameters met

### 🗄️ **Complete PostgreSQL Integration**

| Table | Purpose | Key Insights |
|-------|---------|--------------|
| **users** | Student profiles | Learning styles, grade levels |
| **conversations** | Chat sessions | Usage patterns, engagement |
| **chat_messages** | Message history | Conversation flow analysis |
| **parameter_extractions** | Inference analytics | AI accuracy tracking |
| **tool_executions** | Tool usage logs | Performance metrics |

### 📊 **Educational Logging System**

<table>
<tr>
<td width="50%">

**Before (Plain Logs)**
```
INFO: Processing request
INFO: Intent: flashcard_generator
INFO: Extracted params: {...}
INFO: Tool executed
```

</td>
<td width="50%">

**After (Educational Logs)**
```
🔍 INTENT CLASSIFICATION
   Tool: flashcard_generator
   Confidence: 95%
   Reasoning: User explicitly mentioned...

🧠 PARAMETER EXTRACTION
   ✓ Extracted: topic, subject
   ✓ Inferred: difficulty=easy
   💡 Why: User said "struggling"

⚡ EXECUTION (2.5s)
   ✅ Generated 5 flashcards!
```

</td>
</tr>
</table>

### 🔄 **LangGraph Workflow Orchestration**

```
                    ┌─────────────────┐
                    │  START: User    │
                    │    Request      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  1. CLASSIFY    │
                    │  Intent + Tool  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  2. EXTRACT     │
                    │  Parameters     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  3. VALIDATE    │
                    │  Schema Check   │
                    └────┬───────┬────┘
                         │       │
                    Valid│       │Missing
                         │       │
                         │  ┌────▼─────┐
                         │  │4a. CLARIFY│
                         │  │Ask User   │
                         │  └────┬─────┘
                         │       │
                    ┌────▼───────▼────┐
                    │ 4b. EXECUTE     │
                    │ Call Tool API   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  5. RESPOND     │
                    │  Return Results │
                    └─────────────────┘
```

---

## 🏗️ Architecture

<div align="center">

```
┌─────────────────────────────────────────────────────────────────┐
│                          STUDENT                                │
│                 (Natural Language Input)                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              FASTAPI ORCHESTRATOR (Port 8000)                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           LangGraph Workflow Engine                    │    │
│  │                                                         │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  Node 1: Intent Classification               │     │    │
│  │  │  → Gemini 1.5 Flash AI                       │     │    │
│  │  │  → 90-100% confidence scoring                │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  │                                                         │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  Node 2: Parameter Extraction                │     │    │
│  │  │  → Extract from message                      │     │    │
│  │  │  → Infer from context/profile                │     │    │
│  │  │  → Provide reasoning                         │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  │                                                         │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  Node 3: Validation                          │     │    │
│  │  │  → Pydantic schema check                     │     │    │
│  │  │  → Detect missing params                     │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  │                                                         │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  Node 4: Execution / Clarification           │     │    │
│  │  │  → Call tool API OR ask user                 │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  │                                                         │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  Node 5: Response Generation                 │     │    │
│  │  │  → Format results                            │     │    │
│  │  │  → Educational logging                       │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────┬──────────────────────┬──────────────────────────┘
               │                      │
       ┌───────▼────────┐    ┌───────▼────────┐
       │  Google Gemini │    │  PostgreSQL    │
       │  1.5 Flash AI  │    │   (Supabase)   │
       │                │    │   5 Tables     │
       └────────────────┘    └────────────────┘
               │
       ┌───────▼────────┐
       │  Tools Service │
       │   (Port 8001)  │
       │                │
       │ • Flashcards   │
       │ • Notes        │
       │ • Explainer    │
       └────────────────┘
```

</div>

### **Data Flow**

1. **📥 Input**: Student sends natural language request
2. **🤖 AI Processing**: Gemini classifies intent and extracts parameters
3. **🔍 Validation**: Pydantic checks all required fields
4. **⚡ Execution**: Calls appropriate tool API
5. **💾 Persistence**: Saves to PostgreSQL (analytics)
6. **📤 Response**: Returns formatted results with educational logging

---

## 🛠️ Tech Stack

### **Backend Core**

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.100+ | High-performance async web framework |
| **LangGraph** | 0.0.65 | State machine workflow orchestration |
| **Google Gemini** | 1.5 Flash | Natural language understanding & AI |
| **PostgreSQL** | 15+ | Relational database (hosted on Supabase) |
| **SQLAlchemy** | 2.0+ | Async ORM for database operations |
| **Pydantic** | 2.0+ | Data validation and schema definition |

### **AI & ML Stack**

| Technology | Purpose |
|------------|---------|
| **LangChain** | AI agent framework and utilities |
| **Google Generative AI** | Gemini model integration |
| **Async Processing** | Non-blocking AI operations |

### **Database & Persistence**

| Component | Details |
|-----------|---------|
| **Database** | PostgreSQL 15+ (Supabase hosted) |
| **Connection** | asyncpg async driver |
| **ORM** | SQLAlchemy 2.0 with async support |
| **Tables** | 5 tables tracking all operations |
| **Migrations** | Automatic schema initialization |

### **Development Tools**

| Tool | Purpose |
|------|---------|
| **Uvicorn** | ASGI server for FastAPI |
| **Python-dotenv** | Environment variable management |
| **Asyncio** | Async/await pattern support |
| **Type Hints** | Full Python typing support |

### **External APIs**

- **Google Gemini AI**: Intent classification and parameter extraction
- **Supabase**: PostgreSQL database hosting
- **Educational Tools API**: Flashcard, note, and concept explanation generation

---

## 📦 Installation & Setup

### **Prerequisites**

| Requirement | Minimum Version | Download |
|-------------|-----------------|----------|
| **Python** | 3.11+ | [python.org](https://python.org) |
| **PostgreSQL** | 15+ | [postgresql.org](https://postgresql.org) or [Supabase](https://supabase.com) |
| **Google API Key** | Latest | [ai.google.dev](https://ai.google.dev) |
| **Git** | Latest | [git-scm.com](https://git-scm.com) |

### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/legendarypotato.git
cd legendarypotato/backend
```

### **2. Create Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
```
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
langgraph>=0.0.65
langchain>=0.1.0
google-generativeai>=0.3.0
sqlalchemy>=2.0.0
asyncpg>=0.28.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

### **4. Set Up Environment Variables**

```bash
# Copy example configuration
cp .env.example .env

# Edit .env file (use your favorite editor)
notepad .env  # Windows
nano .env     # Mac/Linux
```

**Required Configuration (.env):**

```ini
# ============================================
# GOOGLE GEMINI AI (REQUIRED)
# ============================================
# Get your key from: https://ai.google.dev/
GOOGLE_API_KEY=your_api_key_here

# ============================================
# DATABASE CONNECTION (REQUIRED)
# ============================================
# Option 1: Supabase (Recommended)
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database

# Option 2: Local PostgreSQL
# DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ai_tutor

# ============================================
# OPTIONAL: SUPABASE CREDENTIALS
# ============================================
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# ============================================
# APPLICATION SETTINGS
# ============================================
APP_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### **5. Initialize Database**

```bash
python scripts/init_db.py
```

**Expected Output:**
```
✅ Database connection successful
✅ Creating tables...
✅ All 5 tables created successfully:
   ├─ users
   ├─ conversations
   ├─ chat_messages
   ├─ parameter_extractions
   └─ tool_executions
✅ Database initialized successfully!
```

### **6. Verify Installation**

```bash
python scripts/verify_system.py
```

**Expected Output:**
```
========================================
   🔍 SYSTEM VERIFICATION
========================================

Test 1: Config Module ✅
Test 2: Database Connection ✅
Test 3: All Repositories (5/5) ✅
Test 4: Pydantic Schemas ✅
Test 5: Gemini AI Service ✅
Test 6: LangGraph Workflow ✅
Test 7: Educational Logger ✅
Test 8: API Routes (4 routes) ✅
Test 9: FastAPI App ✅
Test 10: Scripts (3/3) ✅

========================================
   ✅ ALL SYSTEMS OPERATIONAL
========================================
```

---

## 🚀 Running the Application

### **Method 1: Quick Start (Recommended)**

Open **3 terminal windows**:

**Terminal 1: Start Tools Service**
```powershell
cd backend
uvicorn scripts.run_tools_service:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2: Start Orchestrator**
```powershell
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 3: Run Interactive Demo**
```powershell
cd backend
python scripts\demo.py
```

### **Method 2: Using Python Scripts**

**Terminal 1:**
```powershell
python scripts\run_tools_service.py
```

**Terminal 2:**
```powershell
python main.py
```

**Terminal 3:**
```powershell
python scripts\demo.py
```

### **Expected Outputs**

**Tools Service (Port 8001):**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Orchestrator (Port 8000):**
```
INFO:     Starting AI Tutor Orchestrator v1.0.0...
INFO:     ✅ Database connection successful!
INFO:     ✅ All 5 tables verified
INFO:     ✅ Gemini AI initialized (model: gemini-1.5-flash)
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Interactive Demo:**
```
╔═══════════════════════════════════════════════════════╗
║         🎓 AI TUTOR ORCHESTRATOR DEMO 🎓             ║
║     Intelligent Educational Tool Orchestration       ║
╚═══════════════════════════════════════════════════════╝

👤 Let's set up your profile first!
Name: John Doe
Grade Level (elementary/middle/high/college): college
Learning Style (visual/auditory/kinesthetic/reading): visual

✅ Profile created successfully!

Your message: I'm struggling with calculus derivatives

🔄 Processing your request...

✅ Generated 5 flashcards on derivatives!
```

### **Verify Services**

| Service | URL | Purpose |
|---------|-----|---------|
| **Tools API Docs** | http://localhost:8001/docs | Interactive API documentation |
| **Orchestrator API Docs** | http://localhost:8000/docs | Main API documentation |
| **Health Check (Tools)** | http://localhost:8001/health | Service status |
| **Health Check (Orchestrator)** | http://localhost:8000/health | Service status |

---

## 🎮 Usage Guide

### **Interactive Demo**

The demo script (`scripts/demo.py`) provides the best way to experience the system:

```bash
python scripts\demo.py
```

### **Example Interactions**

#### **Example 1: Simple Flashcard Request**

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

#### **Example 2: Detailed Concept Explanation**

```
Your message: Explain the chain rule in detail with examples

🔍 INTENT CLASSIFICATION
   Tool: concept_explainer
   Confidence: 98%
   
🧠 PARAMETER EXTRACTION
   ✓ Extracted: concept="chain rule", desired_depth="detailed"
   ✓ Inferred: include_examples=true
   💡 Reasoning: User explicitly requested "with examples"
   
⚡ EXECUTION (3.1s)
   ✅ Generated comprehensive explanation!
```

#### **Example 3: Ambiguous Request (Clarification)**

```
Your message: Help me study

🔍 INTENT CLASSIFICATION
   Tool: unclear (confidence: 45%)
   
❓ CLARIFICATION NEEDED
   What subject would you like to study?
   What type of help do you need?
     • Practice problems (flashcards)
     • Study notes
     • Concept explanation

Your message: Make flashcards for organic chemistry

✅ Now processing with full context...
```

### **Demo Commands**

Type these commands during the demo:

| Command | Description |
|---------|-------------|
| `demo` | Show example questions |
| `stats` | Display session statistics |
| `help` | Show available commands |
| `quit` / `exit` | End session |

---

## 🔬 Technical Details
