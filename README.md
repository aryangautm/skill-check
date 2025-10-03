# Skill Check - AI-Powered Resume Analysis & MCQ Quiz Platform

A FastAPI-based backend application that analyzes resumes using AI and generates personalized MCQ quizzes based on user experience and selected roles.

## 🚀 Quick Start

**New to the project?** Start here:
- [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes with Docker
- [API Usage Examples](API_USAGE.md) - Learn how to use the API
- [Deployment Guide](DEPLOYMENT.md) - Deploy to production

## Features

- 📄 **Resume Upload & Analysis**: Upload PDF, DOC, DOCX, or TXT files
- 🤖 **AI-Powered Analysis**: Uses Google's Gemini 2.5 Flash to analyze resumes
- 📝 **Personalized Quiz Generation**: Creates MCQ questions using Gemini 2.5 Pro
- 🎯 **Role-Based Questions**: Questions tailored to specific roles (Product Manager, Software Engineer, etc.)
- 📊 **Difficulty Levels**: Easy, Medium, and Hard difficulty options
- 🔄 **Batch Processing**: Questions generated in batches of 3 for optimal performance
- 💾 **PostgreSQL Database**: Persistent storage with SQLAlchemy ORM

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Models**: 
  - Gemini 2.5 Flash (resume analysis)
  - Gemini 2.5 Pro (question generation)
- **Validation**: Pydantic v2
- **File Processing**: PyPDF2, python-docx

## Project Structure

```
skill-check/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── database.py        # Database setup
│   ├── models/
│   │   └── models.py          # SQLAlchemy models
│   ├── schemas/
│   │   └── schemas.py         # Pydantic schemas
│   ├── routes/
│   │   └── resume.py          # API endpoints
│   ├── services/
│   │   ├── ai_service.py      # AI integration
│   │   └── file_processor.py  # File handling
│   └── main.py                # FastAPI app
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL database
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/aryangautm/skill-check.git
cd skill-check
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/skillcheck
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
ENVIRONMENT=development
```

5. Set up the database:
```bash
# Create PostgreSQL database
createdb skillcheck

# The tables will be created automatically when you run the app
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Upload Resume
**POST** `/api/upload-resume`

Upload a resume file and get AI analysis.

**Request:**
- `file`: Resume file (PDF, DOC, DOCX, or TXT)

**Response:**
```json
{
  "session_id": 1,
  "resume_summary": "Experienced software engineer with 5 years...",
  "suggested_role": "Senior Software Engineer"
}
```

### 2. Get Resume Summary
**GET** `/api/resume-summary/{session_id}`

Retrieve the resume summary for a session.

**Response:**
```json
{
  "id": 1,
  "resume_summary": "Experienced software engineer...",
  "suggested_role": "Senior Software Engineer",
  "selected_role": null,
  "difficulty_level": null,
  "created_at": "2024-01-01T00:00:00"
}
```

### 3. Generate Questions
**POST** `/api/generate-questions`

Generate MCQ questions for a session.

**Request:**
```json
{
  "session_id": 1,
  "role": "Software Engineer",
  "difficulty": "medium"
}
```

**Response:**
```json
{
  "session_id": 1,
  "questions": [
    {
      "id": 1,
      "question_text": "What is the time complexity...",
      "options": [
        {"label": "A", "option": "O(1)"},
        {"label": "B", "option": "O(n)"},
        {"label": "C", "option": "O(log n)"},
        {"label": "D", "option": "O(n²)"}
      ],
      "correct_answer": "B",
      "explanation": "...",
      "batch_number": 1
    }
  ],
  "batch_number": 1,
  "total_batches": 1
}
```

### 4. Get Questions
**GET** `/api/questions/{session_id}?batch_number={batch_number}`

Retrieve questions for a session.

**Query Parameters:**
- `batch_number` (optional): Get specific batch of questions

**Response:**
```json
{
  "session_id": 1,
  "questions": [...],
  "batch_number": 1,
  "total_batches": 3
}
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Schema

### Sessions Table
- `id`: Primary key
- `user_name`: Optional user name
- `resume_text`: Extracted resume text
- `resume_summary`: AI-generated summary
- `suggested_role`: AI-suggested role
- `selected_role`: User-selected role
- `difficulty_level`: Selected difficulty (easy/medium/hard)
- `created_at`: Timestamp

### Questions Table
- `id`: Primary key
- `session_id`: Foreign key to sessions
- `question_text`: The question
- `options`: JSON array of options
- `correct_answer`: The correct answer
- `explanation`: Explanation for the answer
- `batch_number`: Batch identifier
- `created_at`: Timestamp

## Development

### Run in development mode:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations (using Alembic):
```bash
# Initialize Alembic (if needed)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `GEMINI_API_KEY`: Google Gemini API key
- `SECRET_KEY`: Secret key for the application
- `ENVIRONMENT`: Environment mode (development/production)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Apache License 2.0 - see LICENSE file for details