# backend/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    job_role = Column(String(255), nullable=False)
    questions = Column(Text, nullable=False)   # stored as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
