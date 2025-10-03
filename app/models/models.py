from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=True)
    resume_text = Column(Text, nullable=False)
    resume_summary = Column(Text, nullable=True)
    suggested_role = Column(String, nullable=True)
    selected_role = Column(String, nullable=True)
    difficulty_level = Column(SQLEnum(DifficultyLevel), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    questions = relationship("Question", back_populates="session", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of options
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    batch_number = Column(Integer, nullable=False)  # To track batches
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("Session", back_populates="questions")
