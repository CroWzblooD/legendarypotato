# ⚡ Quick Start Guide

Get the AI Tutor Orchestrator running in **5 minutes**!

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Google Gemini API Key ([Get one here](https://ai.google.dev/))
- [ ] PostgreSQL database OR Supabase account ([Sign up free](https://supabase.com))

---

## Step-by-Step Setup

### 1️⃣ Clone & Setup Environment

```bash
# Clone the repository
git clone https://github.com/CroWzblooD/legendarypotato
cd legendarypotato/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit .env file with your credentials
```

**Required values in `.env`:**

```ini
# Google Gemini AI Key (GET THIS FIRST!)
GOOGLE_API_KEY=your_gemini_api_key_here

# Database Connection String
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database

# Optional: If using Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
```

**How to get credentials:**

**Google Gemini API Key:**
1. Go to [https://ai.google.dev/](https://ai.google.dev/)
2. Click "Get API Key in Google AI Studio"
3. Create new project or select existing
4. Click "Create API Key"
5. Copy and paste into `.env`

**Supabase Database:**
> we used supabase to speed up the development process.
1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start your project"
3. Create a new project (free tier!)
4. Go to **Project Settings** → **Database**
5. Copy "Connection String" (Transaction mode)
6. Paste as `DATABASE_URL` in `.env`
7. Replace `[YOUR-PASSWORD]` with your database password

### 3️⃣ Initialize Database (1 min)

```bash
python scripts/init_db.py
```

**Expected output:**
```
================================================================================
DATABASE INITIALIZATION - AI Tutor Orchestrator
================================================================================

✅ Database connection successful!
✅ All tables created successfully!
✅ All expected tables present!
```

### 4️⃣ Run the Application (1 min)

Open **3 terminals** in the `backend` folder:

**Terminal 1 - Educational Tools Service:**
_This service takes care of all content generation with an LLM as a final step._
```bash
python scripts/run_tools_service.py
```
Wait for: `Uvicorn running on http://0.0.0.0:8001`

**Terminal 2 - Orchestrator Service:**
_This is the brain of the project. It delegates tasks to different modules._
```bash
python main.py
```
Wait for: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 3 - Interactive Demo:**
```bash
python scripts/demo.py
```

---

## 🎉 You're Ready!

The demo will guide you through:
1. Creating a user profile
2. Starting a conversation
3. Seeing the AI orchestration workflow in action

Try asking:
- "I need help with calculus derivatives"
- "Make me flashcards on photosynthesis"
- "Explain the concept of recursion in detail"

---

## 🔧 Verify Everything Works

### Check Services Are Running

1. **Tools Service Health**: [http://localhost:8001/health](http://localhost:8001/health)
   - Should return: `{"status": "healthy"}`

2. **Orchestrator Health**: [http://localhost:8000/](http://localhost:8000/)
   - Should return: `{"service": "AI Tutor Orchestrator", ...}`

3. **Interactive API Docs**:
   - Tools: [http://localhost:8001/docs](http://localhost:8001/docs)
   - Orchestrator: [http://localhost:8000/docs](http://localhost:8000/docs)

### Test with API

```bash
# Test orchestrator endpoint
curl -X POST "http://localhost:8000/api/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need practice with derivatives",
    "user_info": {
      "user_id": "test-123",
      "name": "Test User",
      "grade_level": "college",
      "learning_style_summary": "Visual learner",
      "emotional_state_summary": "Ready to learn",
      "mastery_level_summary": "Intermediate",
      "teaching_style": "visual"
    },
    "chat_history": [],
    "conversation_id": "test-conv-123"
  }'
```

---

## ❌ Troubleshooting Common Issues

### Issue: "ModuleNotFoundError: No module named 'config'"

**Solution:**
```bash
# Make sure you're in the backend folder
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Database connection failed"

**Solution 1:** Check your DATABASE_URL in `.env`
```bash
# Test connection manually
python scripts/init_db.py
```

**Solution 2:** If using Supabase, make sure:
- Project is not paused (Supabase free tier pauses after inactivity)
- Password in connection string matches your database password
- Using **Transaction mode** connection string (not Session)

### Issue: "Invalid API key" (Gemini)

**Solution:**
1. Double-check `GOOGLE_API_KEY` in `.env` has no extra spaces
2. Generate a fresh API key from [https://ai.google.dev/](https://ai.google.dev/)
3. Make sure API is enabled for your Google Cloud project

### Issue: "Port already in use"

**Solution:**
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Issue: Import errors after file reorganization

**Solution:**
```bash
# Clear Python cache
# Windows:
Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force

# Mac/Linux:
find . -type d -name __pycache__ -exec rm -rf {} +

# Restart Python interpreter
deactivate
venv\Scripts\activate  # Windows
```

---

## 📚 Next Steps

Now that you're running:

1. **Try the Interactive Demo** (`scripts/demo.py`)
   - See the AI workflow in action
   - Test different types of requests
   - View educational logging

2. **Explore API Documentation**
   - Orchestrator: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Tools: [http://localhost:8001/docs](http://localhost:8001/docs)

3. **Check Database**
   - Use TablePlus, pgAdmin, or Supabase dashboard
   - See how conversations are stored
   - Analyze parameter extraction accuracy

4. **Read Full Documentation**
   - See [README.md](README.md) for complete guide
   - Understand the architecture
   - Learn about each component

---

## 🎯 Example Requests to Try

### 1. Flashcard Generation
```
"I'm struggling with calculus derivatives and need some practice problems"
```

**What happens:**
- Intent: flashcard_generator (95% confidence)
- Extracted: topic="derivatives", subject="calculus"
- Inferred: difficulty="easy" (from "struggling"), count=5
- Result: 5 flashcards generated in ~2.5s

### 2. Note Making
```
"Create study notes on photosynthesis for my biology class"
```

**What happens:**
- Intent: note_maker (98% confidence)
- Extracted: topic="photosynthesis", subject="biology"
- Inferred: note_taking_style="structured", include_examples=true
- Result: Structured notes with 4 sections in ~4.5s

### 3. Concept Explanation
```
"I don't understand the chain rule in calculus, can you explain it?"
```

**What happens:**
- Intent: concept_explainer (96% confidence)
- Extracted: concept="chain rule", current_topic="calculus"
- Inferred: desired_depth="basic", include_examples=true
- Result: Detailed explanation with examples in ~3.2s

---

## 💡 Pro Tips

1. **Watch the Educational Logs**: The color-coded output shows exactly what the AI is doing at each step

2. **Check Database Tables**: All interactions are saved - great for analytics

3. **Use the Stats Command**: Type `stats` in the demo to see inference accuracy

4. **Try Edge Cases**: Ask ambiguous questions to see the clarification system

5. **Test Different Profiles**: Change grade level and learning style to see adaptations

---

## 🆘 Need Help?

- **GitHub Issues**: Report bugs or ask questions
- **API Docs**: Interactive Swagger UI at `/docs` endpoints
- **Full README**: [README.md](README.md) for complete documentation

---

**Ready to build something amazing? Let's go! 🚀**
