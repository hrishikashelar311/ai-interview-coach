# 🎯 AI Interview Coach

An AI-powered interview preparation tool that generates role-specific interview questions and evaluates your answers with detailed feedback — built with FastAPI, React, and OpenAI.

**Live Demo:** [ai-interview-coach-swart.vercel.app](https://ai-interview-coach-swart.vercel.app)

---

## What It Does

- Enter any job role (e.g. "Java Backend Engineer", "React Developer", "Product Manager")
- Get 5 AI-generated interview questions tailored to that role
- Type or speak your answer to each question
- Receive an AI score (1–10), detailed feedback, and specific improvement suggestions

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Axios, CSS3 |
| Backend | Python, FastAPI, SQLAlchemy |
| Database | MySQL (Aiven Cloud) |
| AI | OpenAI GPT-4o-mini |
| Deployment | Vercel (frontend), Railway (backend) |
| Version Control | Git, GitHub |

---

## Project Structure

```
ai-interview-coach/
├── backend/
│   ├── main.py          # FastAPI app, API endpoints, CORS config
│   ├── database.py      # SQLAlchemy engine and session management
│   ├── models.py        # Database table definitions (ORM models)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── requirements.txt # Python dependencies
│   └── .env             # Environment variables (not committed)
├── frontend/
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   └── App.css      # Styles
│   └── .env             # Frontend environment variables (not committed)
└── README.md
```

---

## API Endpoints

### `POST /generate-questions`
Takes a job role and returns 5 AI-generated interview questions. Saves the session to the database.

**Request:**
```json
{
  "job_role": "Java Backend Engineer"
}
```

**Response:**
```json
{
  "session_id": 1,
  "job_role": "Java Backend Engineer",
  "questions": [
    "Explain the difference between JDK, JRE, and JVM.",
    "How does Spring Boot auto-configuration work?",
    "..."
  ]
}
```

---

### `POST /evaluate-answer`
Takes a question and candidate answer, returns AI scoring and feedback.

**Request:**
```json
{
  "session_id": 1,
  "question": "Explain the difference between JDK, JRE, and JVM.",
  "answer": "JDK is the development kit, JRE is the runtime environment..."
}
```

**Response:**
```json
{
  "score": 8,
  "feedback": "Good answer covering the key differences. You correctly identified the hierarchy.",
  "improvements": [
    "Mention that JVM is platform-specific while Java bytecode is platform-independent",
    "Add an example of when you would need JDK vs JRE",
    "Briefly mention the role of the class loader in JVM"
  ]
}
```

---

### `GET /session/{session_id}`
Retrieves a saved session with all questions.

---

## Local Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- MySQL (local) or any cloud MySQL instance
- OpenAI API key

### Backend

```bash
# Clone the repo
git clone https://github.com/hrishikashelar311/ai-interview-coach.git
cd ai-interview-coach/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
touch .env
```

Add to `.env`:
```
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/interview_coach
```

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE interview_coach;
CREATE USER 'coach_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON interview_coach.* TO 'coach_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Run the backend
uvicorn main:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

---

### Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start the app
npm start
```

App available at: `http://localhost:3000`

---

## Deployment

### Backend — Railway
1. Connect GitHub repo to Railway
2. Set root directory to `backend`
3. Add environment variables:
   - `OPENAI_API_KEY`
   - `DATABASE_URL`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Database — Aiven
1. Create free MySQL instance on [Aiven](https://aiven.io)
2. Copy the connection string
3. Use as `DATABASE_URL` in Railway environment variables

### Frontend — Vercel
1. Connect GitHub repo to Vercel
2. Set root directory to `frontend`
3. Add environment variable:
   - `REACT_APP_API_URL=https://your-railway-url.railway.app`
4. Deploy

---

## Key Design Decisions

**Why FastAPI over Flask/Django?**
FastAPI is async-native, auto-generates API documentation, has built-in Pydantic validation, and is significantly faster for I/O-bound tasks like calling the OpenAI API.

**Why store questions as JSON in a Text column?**
For this project scope, it avoids unnecessary complexity. In production, a normalized `questions` table with a foreign key to `sessions` would allow better querying and pagination.

**Why GPT-4o-mini?**
It's cheaper and faster than GPT-4o while being more than capable for structured output tasks like generating interview questions and evaluating short answers.

**Why Aiven for MySQL?**
Free managed MySQL with SSL support, no credit card required for the free tier. Avoids the complexity of managing database volumes and networking in Railway.

---

## Future Improvements

- [ ] User authentication with JWT tokens
- [ ] Voice input using Web Speech API
- [ ] Session history — review past interview performance
- [ ] Score trend dashboard over time
- [ ] LangChain integration for multi-step prompt chains
- [ ] Rate limiting to control OpenAI API costs
- [ ] Support for custom question sets per company

---

## Author

**Hrishika Shelar**
- MS in Computer Science — Illinois Institute of Technology
- MS in AI (in progress)
- 5+ years experience in Software Engineering

[LinkedIn](https://linkedin.com/in/hrishikashelar) | [GitHub](https://github.com/hrishikashelar311)
