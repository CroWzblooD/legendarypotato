# AI Tutor Orchestrator - Backend

Intelligent middleware for autonomous educational tool orchestration using LangGraph and Google Gemini.

## Architecture

```
┌─────────────────────────────────────────────┐
│         LangGraph Workflow                  │
│                                              │
│  1. Intent Classification (Gemini)          │
│  2. Parameter Extraction (Gemini)           │
│  3. Schema Validation (Pydantic)            │
│  4. Tool Execution (HTTP)                   │
│  5. Response Formatting                     │
└─────────────────────────────────────────────┘
```

## Project Structure

```
backend/
├── agents/              # Orchestration agents
│   ├── validator.py     # Parameter validation
│   └── tool_executor.py # Tool API calls
├── api/                 # FastAPI routes
│   └── routes.py        # Main endpoints
├── graph/               # LangGraph workflow
│   └── workflow.py      # State graph definition
├── models/              # Pydantic schemas
│   └── schemas.py       # All data models
├── services/            # External services
│   └── gemini_service.py # Gemini AI integration
├── config.py            # Configuration management
├── main.py              # Main orchestrator app
├── tools_main.py        # Educational tools app
└── requirements.txt     # Dependencies
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Run Services

**Terminal 1 - Educational Tools Service (Port 8001):**

```bash
python tools_main.py
```

**Terminal 2 - Orchestrator Service (Port 8000):**

```bash
python main.py
```

## API Endpoints

### Orchestrator Service (Port 8000)

#### POST `/api/chat`

Main chat endpoint for student interactions.

**Request:**
```json
{
  "message": "I'm struggling with calculus derivatives, need practice",
  "user_info": {
    "user_id": "student123",
    "name": "Alex",
    "grade_level": "11",
    "learning_style_summary": "Visual learner",
    "emotional_state_summary": "Confused but motivated",
    "mastery_level_summary": "Level 5: Building competence"
  },
  "chat_history": [],
  "conversation_id": null
}
```

**Response:**
```json
{
  "conversation_id": "uuid",
  "message": "Tool executed successfully. Here are your results:",
  "tool_response": {
    "tool_type": "flashcard_generator",
    "success": true,
    "data": { ... },
    "execution_time_ms": 250
  },
  "extracted_parameters": {
    "tool_type": "flashcard_generator",
    "parameters": {
      "topic": "derivatives",
      "count": 5,
      "difficulty": "easy",
      "subject": "calculus"
    },
    "confidence": 0.9,
    "inferred_params": {
      "difficulty": "easy"
    }
  },
  "needs_clarification": false
}
```

#### GET `/api/health`

Health check endpoint.

#### GET `/api/tools`

List available educational tools.

### Educational Tools Service (Port 8001)

#### POST `/api/note-maker`

Generate study notes.

#### POST `/api/flashcard-generator`

Generate flashcards.

#### POST `/api/concept-explainer`

Explain concepts.

## Key Features

### 1. Intelligent Parameter Extraction

Multi-layer extraction strategy:

- **Explicit**: Directly stated parameters
- **Inference**: Context-based deduction
  - "struggling" → difficulty: "easy"
  - "practice" → tool: flashcard_generator
- **History**: Multi-turn context tracking
- **Defaults**: Smart fallbacks based on profile

### 2. Personalization

Adapts to:
- **Mastery Level**: Adjusts depth and difficulty
- **Emotional State**: Modifies tone and complexity
- **Teaching Style**: Changes explanation approach
- **Learning Preferences**: Customizes format

### 3. Validation

- Pydantic schema validation
- Required parameter checking
- Type enforcement
- Range validation

### 4. Error Handling

- Graceful degradation
- Clarification questions
- Retry logic
- Detailed logging

## Testing

### Test with cURL

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create 5 flashcards on photosynthesis",
    "user_info": {
      "user_id": "test123",
      "name": "Test Student",
      "grade_level": "9",
      "learning_style_summary": "Kinesthetic learner",
      "emotional_state_summary": "Focused",
      "mastery_level_summary": "Level 6"
    }
  }'
```

### Interactive API Docs

Visit http://localhost:8000/docs for Swagger UI.

## Development

### Adding a New Tool

1. Add tool schema in `models/schemas.py`
2. Add validation in `agents/validator.py`
3. Add tool type to enum
4. Create tool endpoint in `tools_main.py`
5. Update extraction prompts in `services/gemini_service.py`

### Logging

Logs are configured in `main.py`. Adjust `LOG_LEVEL` in `.env`:

```
LOG_LEVEL=DEBUG  # For detailed logs
LOG_LEVEL=INFO   # For standard logs
LOG_LEVEL=ERROR  # For errors only
```

## Deployment

### Local

Already configured for local development.

### Production

1. Set `APP_ENV=production` in `.env`
2. Set `DEBUG=False`
3. Use proper database (PostgreSQL instead of SQLite)
4. Set up reverse proxy (nginx)
5. Use process manager (PM2, systemd)

### Docker (Optional)

```bash
docker build -t ai-tutor-orchestrator .
docker run -p 8000:8000 ai-tutor-orchestrator
```

## Troubleshooting

### Gemini API Errors

- Check API key is valid
- Check rate limits (15 requests/min free tier)
- Check model name is correct

### Tool Connection Errors

- Ensure tools service is running on port 8001
- Check `TOOL_SERVICE_URL` in `.env`
- Verify CORS settings

### Import Errors

- Ensure all dependencies installed
- Check Python version (3.11+)
- Verify virtual environment activated

## License

MIT
