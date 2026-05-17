# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from openai import OpenAI
from dotenv import load_dotenv
import os, json

from database import get_db, engine
from models import Base, Session as SessionModel
from schemas import QuestionRequest, QuestionResponse, AnswerRequest, AnswerFeedback

load_dotenv()

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Interview Coach")

# Allow React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/")
def root():
    return {"message": "AI Interview Coach API is running"}


@app.post("/generate-questions", response_model=QuestionResponse)
def generate_questions(request: QuestionRequest, db: Session = Depends(get_db)):
    """Takes job role, returns 5 interview questions, saves session to DB"""
    
    prompt = f"""You are an expert technical interviewer. Generate exactly 5 interview questions 
    for a {request.job_role} position. 
    Mix technical and behavioral questions.
    Return ONLY a JSON array of 5 strings. No extra text. Example:
    ["Question 1?", "Question 2?", "Question 3?", "Question 4?", "Question 5?"]"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    raw = response.choices[0].message.content.strip()
    
    try:
        questions = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="OpenAI returned invalid format")
    
    # Save to database
    db_session = SessionModel(
        job_role=request.job_role,
        questions=json.dumps(questions)
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return QuestionResponse(
        session_id=db_session.id,
        job_role=request.job_role,
        questions=questions
    )


@app.post("/evaluate-answer", response_model=AnswerFeedback)
def evaluate_answer(request: AnswerRequest, db: Session = Depends(get_db)):
    """Takes question + answer, returns score and feedback"""
    
    # Verify session exists
    session = db.query(SessionModel).filter(SessionModel.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    prompt = f"""You are an expert interviewer evaluating a candidate's answer.
    
Question: {request.question}
Candidate's Answer: {request.answer}

Evaluate this answer and return ONLY valid JSON in this exact format:
{{
  "score": <integer 1-10>,
  "feedback": "<2-3 sentence overall assessment>",
  "improvements": ["<improvement 1>", "<improvement 2>", "<improvement 3>"]
}}"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=400
    )
    
    raw = response.choices[0].message.content.strip()
    
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response")
    
    return AnswerFeedback(**result)


@app.get("/session/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Retrieve a saved session"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "id": session.id,
        "job_role": session.job_role,
        "questions": json.loads(session.questions),
        "created_at": session.created_at
    }
