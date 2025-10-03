# API Usage Examples

This document provides examples of how to use the Skill Check API.

## Table of Contents
1. [Setup](#setup)
2. [Upload Resume](#upload-resume)
3. [Generate Questions](#generate-questions)
4. [Get Questions](#get-questions)

## Setup

Before making API requests, ensure:
1. The API server is running (`./start.sh` or `uvicorn app.main:app --reload`)
2. Your `.env` file is configured with valid credentials
3. PostgreSQL database is running

## Upload Resume

Upload a resume file (PDF, DOC, DOCX, or TXT) and get AI analysis.

### cURL Example

```bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/resume.pdf"
```

### Python Example

```python
import requests

url = "http://localhost:8000/api/upload-resume"
files = {'file': open('resume.pdf', 'rb')}

response = requests.post(url, files=files)
data = response.json()

print(f"Session ID: {data['session_id']}")
print(f"Summary: {data['resume_summary']}")
print(f"Suggested Role: {data['suggested_role']}")
```

### JavaScript Example

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/upload-resume', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Session ID:', data.session_id);
  console.log('Summary:', data.resume_summary);
  console.log('Suggested Role:', data.suggested_role);
});
```

### Response Example

```json
{
  "session_id": 1,
  "resume_summary": "Experienced software engineer with 5 years of full-stack development expertise in Python, JavaScript, and cloud technologies. Strong background in building scalable web applications.",
  "suggested_role": "Senior Software Engineer"
}
```

## Generate Questions

Generate MCQ questions for a session based on role and difficulty.

### cURL Example

```bash
curl -X POST "http://localhost:8000/api/generate-questions" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "role": "Software Engineer",
    "difficulty": "medium"
  }'
```

### Python Example

```python
import requests

url = "http://localhost:8000/api/generate-questions"
payload = {
    "session_id": 1,
    "role": "Software Engineer",
    "difficulty": "medium"
}

response = requests.post(url, json=payload)
data = response.json()

print(f"Batch Number: {data['batch_number']}")
print(f"Total Questions: {len(data['questions'])}")

for question in data['questions']:
    print(f"\nQ: {question['question_text']}")
    for option in question['options']:
        print(f"  {option['label']}: {option['option']}")
    print(f"Answer: {question['correct_answer']}")
```

### JavaScript Example

```javascript
fetch('http://localhost:8000/api/generate-questions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    session_id: 1,
    role: 'Software Engineer',
    difficulty: 'medium'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Questions:', data.questions);
  console.log('Batch Number:', data.batch_number);
});
```

### Response Example

```json
{
  "session_id": 1,
  "questions": [
    {
      "id": 1,
      "question_text": "What is the time complexity of binary search?",
      "options": [
        {"label": "A", "option": "O(1)"},
        {"label": "B", "option": "O(log n)"},
        {"label": "C", "option": "O(n)"},
        {"label": "D", "option": "O(n²)"}
      ],
      "correct_answer": "B",
      "explanation": "Binary search divides the search space in half at each step, resulting in logarithmic time complexity.",
      "batch_number": 1
    },
    {
      "id": 2,
      "question_text": "Which design pattern is used to create a single instance of a class?",
      "options": [
        {"label": "A", "option": "Factory Pattern"},
        {"label": "B", "option": "Singleton Pattern"},
        {"label": "C", "option": "Observer Pattern"},
        {"label": "D", "option": "Strategy Pattern"}
      ],
      "correct_answer": "B",
      "explanation": "The Singleton Pattern ensures a class has only one instance and provides a global point of access to it.",
      "batch_number": 1
    },
    {
      "id": 3,
      "question_text": "What HTTP status code indicates a successful resource creation?",
      "options": [
        {"label": "A", "option": "200 OK"},
        {"label": "B", "option": "201 Created"},
        {"label": "C", "option": "204 No Content"},
        {"label": "D", "option": "202 Accepted"}
      ],
      "correct_answer": "B",
      "explanation": "201 Created indicates that the request has been fulfilled and resulted in a new resource being created.",
      "batch_number": 1
    }
  ],
  "batch_number": 1,
  "total_batches": 1
}
```

## Get Questions

Retrieve questions for a session. Optionally filter by batch number.

### cURL Example

```bash
# Get all questions for a session
curl -X GET "http://localhost:8000/api/questions/1" \
  -H "accept: application/json"

# Get questions for a specific batch
curl -X GET "http://localhost:8000/api/questions/1?batch_number=1" \
  -H "accept: application/json"
```

### Python Example

```python
import requests

# Get all questions
url = "http://localhost:8000/api/questions/1"
response = requests.get(url)
data = response.json()

# Get specific batch
url = "http://localhost:8000/api/questions/1?batch_number=1"
response = requests.get(url)
batch_data = response.json()

print(f"Questions in batch {batch_data['batch_number']}: {len(batch_data['questions'])}")
```

### JavaScript Example

```javascript
// Get all questions
fetch('http://localhost:8000/api/questions/1')
  .then(response => response.json())
  .then(data => {
    console.log('All questions:', data.questions);
  });

// Get specific batch
fetch('http://localhost:8000/api/questions/1?batch_number=1')
  .then(response => response.json())
  .then(data => {
    console.log('Batch questions:', data.questions);
  });
```

## Get Resume Summary

Retrieve the resume summary for a session.

### cURL Example

```bash
curl -X GET "http://localhost:8000/api/resume-summary/1" \
  -H "accept: application/json"
```

### Python Example

```python
import requests

url = "http://localhost:8000/api/resume-summary/1"
response = requests.get(url)
data = response.json()

print(f"Resume Summary: {data['resume_summary']}")
print(f"Suggested Role: {data['suggested_role']}")
print(f"Selected Role: {data['selected_role']}")
print(f"Difficulty Level: {data['difficulty_level']}")
```

### Response Example

```json
{
  "id": 1,
  "resume_summary": "Experienced software engineer with 5 years of full-stack development expertise...",
  "suggested_role": "Senior Software Engineer",
  "selected_role": "Software Engineer",
  "difficulty_level": "medium",
  "created_at": "2024-01-15T10:30:00"
}
```

## Complete Workflow Example

Here's a complete Python example showing the entire workflow:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Step 1: Upload resume
print("Step 1: Uploading resume...")
with open('resume.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{BASE_URL}/upload-resume", files=files)
    upload_data = response.json()
    session_id = upload_data['session_id']
    
print(f"Session ID: {session_id}")
print(f"Summary: {upload_data['resume_summary']}")
print(f"Suggested Role: {upload_data['suggested_role']}")

# Step 2: Generate questions
print("\nStep 2: Generating questions...")
question_request = {
    "session_id": session_id,
    "role": "Software Engineer",
    "difficulty": "medium"
}
response = requests.post(f"{BASE_URL}/generate-questions", json=question_request)
questions_data = response.json()

print(f"Generated {len(questions_data['questions'])} questions")

# Step 3: Display questions
print("\nStep 3: Questions:")
for i, question in enumerate(questions_data['questions'], 1):
    print(f"\nQuestion {i}: {question['question_text']}")
    for option in question['options']:
        marker = "✓" if option['label'] == question['correct_answer'] else " "
        print(f"  [{marker}] {option['label']}: {option['option']}")
    print(f"Explanation: {question['explanation']}")

# Step 4: Get session summary
print("\nStep 4: Getting session summary...")
response = requests.get(f"{BASE_URL}/resume-summary/{session_id}")
summary_data = response.json()
print(f"Session created at: {summary_data['created_at']}")
print(f"Difficulty selected: {summary_data['difficulty_level']}")
```

## Error Handling

The API returns standard HTTP status codes and JSON error messages.

### Example Error Response

```json
{
  "detail": "Session not found"
}
```

### Common Status Codes

- `200 OK`: Success
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input (e.g., unsupported file type)
- `404 Not Found`: Resource not found (e.g., invalid session_id)
- `500 Internal Server Error`: Server error (e.g., AI service failure)

### Python Error Handling Example

```python
try:
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raises HTTPError for bad status codes
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response: {e.response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```
