# Quick Start Guide

Get the Skill Check API up and running in 5 minutes!

## 🚀 Quick Setup (Docker - Recommended)

The fastest way to get started is using Docker:

### Prerequisites
- Docker and Docker Compose installed
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/aryangautm/skill-check.git
   cd skill-check
   ```

2. **Set your Gemini API key**
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   export SECRET_KEY="your_secret_key_here"
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

That's it! The API is now running with a PostgreSQL database.

## 🐍 Manual Setup (Without Docker)

### Prerequisites
- Python 3.9+
- PostgreSQL database
- Google Gemini API key

### Steps

1. **Clone and navigate to the repository**
   ```bash
   git clone https://github.com/aryangautm/skill-check.git
   cd skill-check
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and API keys
   ```

5. **Setup database**
   ```bash
   # Create PostgreSQL database
   createdb skillcheck
   
   # Run migrations
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   ./start.sh
   # Or manually: uvicorn app.main:app --reload
   ```

## 📝 First API Request

### Test the API with cURL

```bash
# Check health
curl http://localhost:8000/health

# Upload a resume (replace with your file path)
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@/path/to/resume.pdf"
```

### Test with Python

```python
import requests

# Upload resume
files = {'file': open('resume.pdf', 'rb')}
response = requests.post('http://localhost:8000/api/upload-resume', files=files)
data = response.json()

print(f"Session ID: {data['session_id']}")
print(f"Summary: {data['resume_summary']}")
print(f"Suggested Role: {data['suggested_role']}")

# Generate questions
session_id = data['session_id']
response = requests.post('http://localhost:8000/api/generate-questions', json={
    'session_id': session_id,
    'role': 'Software Engineer',
    'difficulty': 'medium'
})

questions = response.json()
print(f"Generated {len(questions['questions'])} questions")
```

## 🎯 What's Next?

- **Explore the API**: Visit http://localhost:8000/docs for interactive documentation
- **Read detailed examples**: Check out [API_USAGE.md](API_USAGE.md) for more examples
- **Deploy to production**: See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guides
- **Understand the code**: Review [README.md](README.md) for architecture details

## 🔑 Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API key"
4. Copy the API key
5. Add it to your `.env` file or export as environment variable

## 🐛 Troubleshooting

### Port 8000 already in use
```bash
# Kill process using port 8000
kill -9 $(lsof -ti:8000)
# Or use a different port
uvicorn app.main:app --port 8080
```

### Database connection error
- Make sure PostgreSQL is running
- Verify DATABASE_URL in .env file
- For Docker: `docker-compose up db` to check database logs

### Gemini API error
- Verify GEMINI_API_KEY is correct
- Check API quota at https://console.cloud.google.com/
- Ensure you have enabled the Generative AI API

## 📚 Project Structure

```
skill-check/
├── app/                    # Application code
│   ├── core/              # Configuration and database
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic (AI, file processing)
│   └── main.py            # FastAPI app
├── alembic/               # Database migrations
├── API_USAGE.md           # API examples
├── DEPLOYMENT.md          # Deployment guide
├── docker-compose.yml     # Docker setup
├── Dockerfile             # Docker image
└── requirements.txt       # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## 💬 Support

- **Issues**: https://github.com/aryangautm/skill-check/issues
- **Documentation**: http://localhost:8000/docs (when running)
- **Examples**: [API_USAGE.md](API_USAGE.md)

---

Happy coding! 🎉
