# System Architecture

## Overview

This document describes the architecture of the Skill Check API.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          Client Layer                            │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │
│  │  Web App │  │  Mobile  │  │   CLI    │  │  Third Party │    │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └──────┬───────┘    │
└────────┼─────────────┼─────────────┼──────────────┼─────────────┘
         │             │             │              │
         └─────────────┴─────────────┴──────────────┘
                            │
                            ▼
         ┌─────────────────────────────────────┐
         │         CORS Middleware             │
         └─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                         │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    API Routes                               │ │
│  │                                                             │ │
│  │  POST /api/upload-resume          Upload & analyze resume  │ │
│  │  GET  /api/resume-summary/:id     Get session summary     │ │
│  │  POST /api/generate-questions     Generate MCQ questions   │ │
│  │  GET  /api/questions/:id          Get session questions   │ │
│  │  GET  /health                      Health check            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                 Business Logic Layer                        │ │
│  │                                                             │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │ │
│  │  │     File     │  │   Resume     │  │    Question     │ │ │
│  │  │  Processor   │  │   Analyzer   │  │   Generator     │ │ │
│  │  │              │  │              │  │                 │ │ │
│  │  │ - PDF        │  │ - Gemini     │  │ - Gemini        │ │ │
│  │  │ - DOCX       │  │   2.5 Flash  │  │   2.5 Pro       │ │ │
│  │  │ - TXT        │  │ - Summary    │  │ - Batch of 3    │ │ │
│  │  │ - DOC        │  │ - Role       │  │ - Difficulty    │ │ │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  Data Access Layer                          │ │
│  │                                                             │ │
│  │  ┌──────────────┐  ┌──────────────┐                       │ │
│  │  │   Session    │  │   Question   │                       │ │
│  │  │    Model     │  │    Model     │                       │ │
│  │  │              │  │              │                       │ │
│  │  │ - resume     │  │ - text       │                       │ │
│  │  │ - summary    │  │ - options    │                       │ │
│  │  │ - role       │  │ - answer     │                       │ │
│  │  │ - difficulty │  │ - batch #    │                       │ │
│  │  └──────────────┘  └──────────────┘                       │ │
│  │          │                  │                              │ │
│  │          └──────────┬───────┘                              │ │
│  │                     │                                       │ │
│  │                     ▼                                       │ │
│  │          ┌────────────────────┐                            │ │
│  │          │   SQLAlchemy ORM   │                            │ │
│  │          └────────────────────┘                            │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
         ┌─────────────────────────────────────┐
         │        PostgreSQL Database          │
         │                                     │
         │  ┌───────────┐   ┌──────────────┐  │
         │  │  sessions │   │  questions   │  │
         │  └───────────┘   └──────────────┘  │
         └─────────────────────────────────────┘

                            │
                            ▼
         ┌─────────────────────────────────────┐
         │       External Services             │
         │                                     │
         │  ┌──────────────────────────────┐  │
         │  │   Google Gemini AI API       │  │
         │  │                              │  │
         │  │  - gemini-2.0-flash-exp      │  │
         │  │    (Resume Analysis)         │  │
         │  │                              │  │
         │  │  - gemini-2.0-flash-         │  │
         │  │    thinking-exp-01-21        │  │
         │  │    (Question Generation)     │  │
         │  └──────────────────────────────┘  │
         └─────────────────────────────────────┘
```

## Request Flow

### 1. Upload Resume Flow

```
User → Upload PDF/DOC/TXT
  ↓
FastAPI receives file
  ↓
File Processor extracts text
  ↓
Resume Analyzer (Gemini 2.5 Flash)
  ↓
Generate summary & suggested role
  ↓
Save to Session table
  ↓
Return session_id, summary, role
```

### 2. Generate Questions Flow

```
User → Request questions (session_id, role, difficulty)
  ↓
Fetch session from database
  ↓
Question Generator (Gemini 2.5 Pro)
  ↓
Generate 3 MCQ questions in batch
  ↓
Save to Questions table
  ↓
Return questions with batch number
```

### 3. Get Questions Flow

```
User → Request questions (session_id, batch_number?)
  ↓
Query Questions table
  ↓
Filter by session and optional batch
  ↓
Return formatted questions
```

## Component Details

### File Processor
- **Purpose**: Extract text from uploaded files
- **Supported Formats**: PDF, DOCX, DOC, TXT
- **Libraries**: PyPDF2, python-docx
- **Error Handling**: Validates file format, handles extraction errors

### Resume Analyzer
- **Purpose**: Analyze resume and generate summary
- **AI Model**: Gemini 2.5 Flash (fast, efficient)
- **Output**: 
  - Concise summary (2-3 sentences)
  - Suggested role based on experience
- **Lazy Loading**: API key configured on first use

### Question Generator
- **Purpose**: Generate personalized MCQ questions
- **AI Model**: Gemini 2.5 Pro (advanced reasoning)
- **Features**:
  - Role-specific questions
  - Difficulty-based complexity
  - Batch processing (3 questions at a time)
  - Includes explanations
- **Output Format**: JSON with question, options (A-D), answer, explanation

### Database Models

#### Session Model
```python
- id: Primary key
- user_name: Optional user identifier
- resume_text: Extracted resume text
- resume_summary: AI-generated summary
- suggested_role: AI-suggested role
- selected_role: User-selected role
- difficulty_level: easy/medium/hard
- created_at: Timestamp
```

#### Question Model
```python
- id: Primary key
- session_id: Foreign key to Session
- question_text: The question
- options: JSON array [{label, option}]
- correct_answer: Letter (A/B/C/D)
- explanation: Why this is the answer
- batch_number: Batch identifier
- created_at: Timestamp
```

## Technology Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **Python 3.11+**: Programming language

### Database
- **PostgreSQL**: Relational database
- **SQLAlchemy**: ORM
- **Alembic**: Migration tool

### AI/ML
- **Google Gemini API**: Generative AI
- **Models**:
  - gemini-2.0-flash-exp (resume analysis)
  - gemini-2.0-flash-thinking-exp-01-21 (question generation)

### Data Validation
- **Pydantic**: Data validation and settings
- **Pydantic Settings**: Environment configuration

### File Processing
- **PyPDF2**: PDF text extraction
- **python-docx**: Word document processing

## Deployment Options

### Development
- Local setup with virtual environment
- Docker Compose with PostgreSQL

### Production
- Docker containers
- Cloud platforms (AWS, GCP, Heroku, Railway)
- VPS with Nginx reverse proxy
- Kubernetes for scaling

## Security Considerations

1. **Environment Variables**: Sensitive data in .env
2. **CORS**: Configurable allowed origins
3. **Input Validation**: Pydantic schemas
4. **File Upload**: Type and size restrictions
5. **Database**: Parameterized queries via ORM
6. **API Keys**: Secured in environment variables

## Scalability

### Vertical Scaling
- Increase server resources
- Database connection pooling
- Optimize queries

### Horizontal Scaling
- Load balancer
- Multiple API instances
- Shared PostgreSQL database
- Redis for session/cache

### Optimization
- Batch processing for questions
- Async operations
- Database indexing
- Response caching
- CDN for static assets

## Monitoring & Logging

### Health Checks
- `/health` endpoint
- Database connectivity check
- API service status

### Logging
- Request/response logging
- Error tracking
- Performance metrics

### Observability
- Application logs
- Database query logs
- AI API usage tracking
