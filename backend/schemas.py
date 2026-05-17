# backend/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List

class QuestionRequest(BaseModel):
    job_role: str

class QuestionResponse(BaseModel):
    session_id: int
    job_role: str
    questions: List[str]

class AnswerRequest(BaseModel):
    session_id: int
    question: str
    answer: str

class AnswerFeedback(BaseModel):
    score: int          # 1-10
    feedback: str
    improvements: List[str]
