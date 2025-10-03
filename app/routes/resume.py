from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models import Session as SessionModel, Question, DifficultyLevel
from app.schemas import (
    ResumeAnalysisResponse, 
    QuestionGenerationRequest,
    QuestionBatchResponse,
    MCQQuestion,
    MCQOption,
    SessionResponse,
)
from app.services import extract_text_from_file, ResumeAnalyzer, QuestionGenerator

router = APIRouter()
resume_analyzer = ResumeAnalyzer()
question_generator = QuestionGenerator()


@router.post("/upload-resume", response_model=ResumeAnalysisResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a resume file (PDF, DOC, DOCX, or TXT) and get AI analysis.
    Returns a session ID, resume summary, and suggested role.
    """
    # Validate file type
    allowed_extensions = ['pdf', 'doc', 'docx', 'txt']
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Read file content
    file_content = await file.read()
    
    # Extract text from file
    try:
        resume_text = extract_text_from_file(file_content, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
    
    # Analyze resume using AI
    try:
        summary, suggested_role = resume_analyzer.analyze_resume(resume_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")
    
    # Create session in database
    session = SessionModel(
        resume_text=resume_text,
        resume_summary=summary,
        suggested_role=suggested_role
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return ResumeAnalysisResponse(
        session_id=session.id,
        resume_summary=summary,
        suggested_role=suggested_role
    )


@router.get("/resume-summary/{session_id}", response_model=SessionResponse)
async def get_resume_summary(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the resume summary for a specific session.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionResponse(
        id=session.id,
        resume_summary=session.resume_summary,
        suggested_role=session.suggested_role,
        selected_role=session.selected_role,
        difficulty_level=session.difficulty_level.value if session.difficulty_level else None,
        created_at=session.created_at
    )


@router.post("/generate-questions", response_model=QuestionBatchResponse)
async def generate_questions(
    request: QuestionGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate MCQ questions for a session based on role and difficulty.
    Questions are generated in batches of 3.
    """
    # Get session
    session = db.query(SessionModel).filter(SessionModel.id == request.session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Update session with selected role and difficulty
    session.selected_role = request.role
    session.difficulty_level = request.difficulty
    
    # Determine batch number (count existing batches + 1)
    max_batch = db.query(Question).filter(
        Question.session_id == request.session_id
    ).count() // 3 + 1
    
    # Generate questions using AI
    try:
        questions_data = question_generator.generate_questions(
            resume_text=session.resume_text,
            role=request.role,
            difficulty=request.difficulty.value,
            batch_size=3
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")
    
    # Save questions to database
    questions = []
    for q_data in questions_data:
        question = Question(
            session_id=request.session_id,
            question_text=q_data["question_text"],
            options=q_data["options"],
            correct_answer=q_data["correct_answer"],
            explanation=q_data.get("explanation", ""),
            batch_number=max_batch
        )
        db.add(question)
        questions.append(question)
    
    db.commit()
    
    # Refresh to get IDs
    for q in questions:
        db.refresh(q)
    
    # Convert to response format
    mcq_questions = [
        MCQQuestion(
            id=q.id,
            question_text=q.question_text,
            options=[MCQOption(**opt) for opt in q.options],
            correct_answer=q.correct_answer,
            explanation=q.explanation,
            batch_number=q.batch_number
        )
        for q in questions
    ]
    
    return QuestionBatchResponse(
        session_id=request.session_id,
        questions=mcq_questions,
        batch_number=max_batch,
        total_batches=max_batch
    )


@router.get("/questions/{session_id}", response_model=QuestionBatchResponse)
async def get_questions(
    session_id: int,
    batch_number: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get questions for a session. If batch_number is provided, returns that batch.
    Otherwise, returns all questions.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    query = db.query(Question).filter(Question.session_id == session_id)
    
    if batch_number is not None:
        query = query.filter(Question.batch_number == batch_number)
    
    questions = query.all()
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    
    # Get total batches
    total_batches = db.query(Question).filter(
        Question.session_id == session_id
    ).count() // 3
    
    # Convert to response format
    mcq_questions = [
        MCQQuestion(
            id=q.id,
            question_text=q.question_text,
            options=[MCQOption(**opt) for opt in q.options],
            correct_answer=q.correct_answer,
            explanation=q.explanation,
            batch_number=q.batch_number
        )
        for q in questions
    ]
    
    return QuestionBatchResponse(
        session_id=session_id,
        questions=mcq_questions,
        batch_number=batch_number or questions[0].batch_number,
        total_batches=total_batches
    )
