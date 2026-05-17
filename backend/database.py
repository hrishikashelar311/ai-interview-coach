# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Force pymysql driver even if Railway gives mysql:// URL
DATABASE_URL_FIXED = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
engine = create_engine(DATABASE_URL_FIXED)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
