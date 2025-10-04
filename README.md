# 🎓 AI Tutor Orchestrator

**Intelligent Middleware for Autonomous Educational Tool Orchestration**

Built for the AI Agent Engineering Hackathon - Task 2

---

## 🏆 Project Overview

An intelligent orchestration layer that sits between conversational AI tutors and educational tools, autonomously:
- **Classifies** student intent from natural language
- **Extracts** required parameters using multi-layer inference
- **Validates** requests against tool schemas
- **Executes** educational tools (Note Maker, Flashcard Generator, Concept Explainer)
- **Adapts** to student profiles (mastery level, emotional state, teaching style)

### **Key Innovation: 40% Score Focus**
Multi-layer parameter extraction:
1. **Explicit** - Directly stated parameters
2. **Inference** - "struggling" → difficulty: "easy"
3. **Context** - Multi-turn conversation tracking
4. **Profile** - Student mastery/emotion adaptation
5. **Defaults** - Smart fallbacks

---

## 🏗️ Architecture

```
┌──────────────────────┐
│   Next.js Frontend   │  Beautiful chat UI with tool renderers
│     (Port 3000)      │
└──────────┬───────────┘
           │ HTTP
           ↓
┌──────────────────────┐
│  FastAPI Orchestrator│
│     (Port 8000)      │
│                      │
│  ┌────────────────┐ │
│  │  LangGraph     │ │  1. Intent Classification
│  │   Workflow     │ │  2. Parameter Extraction (Gemini)
│  │                │ │  3. Schema Validation (Pydantic)
│  │  Gemini 1.5    │ │  4. Tool Routing
│  │    Flash       │ │  5. Response Processing
│  └────────────────┘ │
└──────────┬───────────┘
           │ HTTP
           ↓
┌──────────────────────┐
│ Educational Tools    │  • Note Maker
│     (Port 8001)      │  • Flashcard Generator
└──────────────────────┘  • Concept Explainer
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API Key (FREE)

### 1. Clone Repository

```bash
cd legendarypotato
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key:
# GOOGLE_API_KEY=your_key_here
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
# or
pnpm install
```

### 4. Run Services

**Terminal 1 - Educational Tools (Port 8001)**
```bash
cd backend
python tools_main.py
```

**Terminal 2 - Orchestrator (Port 8000)**
```bash
cd backend
python main.py
```

**Terminal 3 - Frontend (Port 3000)**
```bash
cd frontend
npm run dev
```

### 5. Open Browser

Visit: **http://localhost:3000**

---

## 🎯 Features

### Core Orchestration
- ✅ **Intent Classification** - Gemini-powered tool selection
- ✅ **Smart Parameter Extraction** - Multi-layer inference engine
- ✅ **Schema Validation** - Pydantic type safety
- ✅ **Tool Execution** - HTTP-based tool integration
- ✅ **Error Recovery** - Clarification questions

### Personalization
- ✅ **Mastery Level Adaptation** - Adjusts difficulty (1-10 scale)
- ✅ **Emotional State** - Responds to confused/anxious/focused states
- ✅ **Teaching Style** - Direct/Socratic/Visual/Flipped
- ✅ **Learning Preferences** - Remembers student choices

### Educational Tools
1. **Note Maker**
   - Structured notes with examples and analogies
   - Adapts style to student preferences
   - Includes practice suggestions

2. **Flashcard Generator**
   - 1-20 cards per request
   - Easy/Medium/Hard difficulty
   - Personalized to mastery level

3. **Concept Explainer**
   - Basic to comprehensive depth
   - Examples and visual aids
   - Practice questions

---

## 📊 Demo Scenarios

### Scenario 1: Direct Request
```
Student: "Create 5 flashcards on photosynthesis at medium difficulty"
```
**System extracts:**
- topic: "photosynthesis"
- count: 5
- difficulty: "medium"
- subject: "Biology" (inferred)

### Scenario 2: Inference Required
```
Student: "I'm struggling with calculus derivatives, need practice"
```
**System infers:**
- tool: flashcard_generator (from "practice")
- difficulty: "easy" (from "struggling")
- topic: "derivatives"
- subject: "calculus"
- count: 5 (default)

### Scenario 3: Multi-Turn Context
```
Turn 1: "I'm in grade 10 studying biology"
Turn 2: "Can you explain photosynthesis?"
```
**System remembers:**
- Uses grade_level from Turn 1
- Maps to mastery level
- Chooses concept_explainer tool

---

## 🧪 Testing

### Test with cURL

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need flashcards on photosynthesis",
    "user_info": {
      "user_id": "test123",
      "name": "Test Student",
      "grade_level": "10",
      "learning_style_summary": "Visual learner",
      "emotional_state_summary": "Focused",
      "mastery_level_summary": "Level 6"
    }
  }'
```

### Interactive API Docs
- Orchestrator: http://localhost:8000/docs
- Tools: http://localhost:8001/docs

---

## 📁 Project Structure

```
legendarypotato/
├── backend/
│   ├── agents/              # Orchestration logic
│   │   ├── validator.py     # Parameter validation
│   │   └── tool_executor.py # Tool API calls
│   ├── api/
│   │   └── routes.py        # FastAPI endpoints
│   ├── graph/
│   │   └── workflow.py      # LangGraph state machine
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   └── gemini_service.py # Gemini AI integration
│   ├── config.py
│   ├── main.py              # Orchestrator app
│   └── tools_main.py        # Tools service
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main chat page
│   │   └── layout.tsx
│   ├── components/
│   │   ├── chat/            # Chat components
│   │   ├── student/         # Profile components
│   │   └── tools/           # Tool renderers
│   └── lib/
│       ├── api.ts           # API client
│       └── types.ts         # TypeScript types
│
├── PROGRESS.md              # Development progress
└── README.md                # This file
```

---

## 🛠️ Technology Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Web framework
- **LangGraph** - Agent orchestration
- **LangChain** - LLM integration
- **Google Gemini 1.5 Flash** - AI model
- **Pydantic v2** - Data validation
- **SQLite** - State storage (optional)

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **Axios** - HTTP client

---

## 🎨 UI Features

- 🎯 **Beautiful Chat Interface** - Modern, responsive design
- 📊 **Tool-Specific Renderers**
  - Accordion notes with collapsible sections
  - Interactive flip flashcards
  - Tabbed explanations
- 👤 **Student Profile Sidebar** - Dynamic profile management
- ⚡ **Real-time Updates** - Instant tool responses
- 🎭 **Loading States** - Typing indicators
- ❌ **Error Handling** - Graceful degradation

---

## 📈 Scoring Alignment

| Criterion | Weight | Implementation |
|-----------|--------|----------------|
| Parameter Extraction | 40% | Multi-layer extraction with Gemini + inference rules |
| Tool Integration | 25% | 3 tools with proper validation and error handling |
| Architecture | 20% | LangGraph workflow, clean separation of concerns |
| UX | 10% | Beautiful UI, natural conversation flow |
| Code Quality | 5% | Type safety, documentation, best practices |

---

## 🐛 Troubleshooting

### Gemini API Errors
```bash
# Check API key
cat backend/.env | grep GOOGLE_API_KEY

# Test API key
curl -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

### Port Already in Use
```bash
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Import Errors
```bash
# Ensure virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

pip install -r requirements.txt
```

---

## 🚢 Deployment

### Backend (Railway/Render)
```bash
# Add Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# Add runtime.txt
python-3.11.0
```

### Frontend (Vercel)
```bash
# Deploy
vercel deploy

# Set environment variables
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

---

## 📝 Documentation

- [Backend README](backend/README.md) - Detailed backend docs
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Architecture Diagram](docs/architecture.md) - System design
- [Demo Scenarios](docs/demo_scenarios.md) - Testing scenarios

---

## 👨‍💻 Development

### Adding a New Tool

1. Add schema in `backend/models/schemas.py`
2. Add validation in `backend/agents/validator.py`
3. Add extraction logic in `backend/services/gemini_service.py`
4. Create endpoint in `backend/tools_main.py`
5. Add renderer in `frontend/components/tools/`

### Environment Variables

**Backend (.env)**
```bash
GOOGLE_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-1.5-flash
APP_PORT=8000
TOOL_SERVICE_URL=http://localhost:8001
```

**Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🎥 Demo Video Script

1. **Introduction** (0:30)
   - Show architecture diagram
   - Explain orchestration concept

2. **Parameter Extraction** (2:00)
   - Direct request demo
   - Inference demo ("struggling" → easy)
   - Multi-turn context demo

3. **Tool Integration** (1:30)
   - Note Maker with beautiful rendering
   - Flashcards with interaction
   - Concept Explainer with tabs

4. **Advanced Features** (1:00)
   - Personalization adaptation
   - Error handling
   - Clarification questions

5. **Technical Highlights** (0:30)
   - LangGraph workflow
   - Scalability to 80+ tools

---

## 📄 License

MIT License - Feel free to use for educational purposes

---

## 🙏 Acknowledgments

- Google Gemini for powerful AI capabilities
- LangChain/LangGraph for orchestration framework
- Vercel for Next.js and deployment
- shadcn/ui for beautiful components

---

## 📧 Contact

For questions or issues, please create an issue in the repository.

---

**Built with ❤️ for the AI Agent Engineering Hackathon**

*Demonstrating the power of intelligent orchestration in educational technology*
