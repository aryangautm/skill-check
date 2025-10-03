from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ResumeAnalysisResponse(BaseModel):
    session_id: int
    resume_summary: str
    suggested_role: str
    
    class Config:
        from_attributes = True


class QuestionGenerationRequest(BaseModel):
    session_id: int
    role: str
    difficulty: DifficultyLevel


class MCQOption(BaseModel):
    option: str
    label: str  # A, B, C, D


class MCQQuestion(BaseModel):
    id: int
    question_text: str
    options: List[MCQOption]
    correct_answer: str
    explanation: Optional[str] = None
    batch_number: int
    
    class Config:
        from_attributes = True


class QuestionBatchResponse(BaseModel):
    session_id: int
    questions: List[MCQQuestion]
    batch_number: int
    total_batches: int


class SessionResponse(BaseModel):
    id: int
    resume_summary: Optional[str] = None
    suggested_role: Optional[str] = None
    selected_role: Optional[str] = None
    difficulty_level: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
