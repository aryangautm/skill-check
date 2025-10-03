# Sample Resume for Testing

This directory contains sample resume files you can use to test the API.

## Sample Resume Text

You can create a file called `sample_resume.txt` with this content:

```
JOHN DOE
Software Engineer

Email: john.doe@email.com
Phone: +1 (555) 123-4567
Location: San Francisco, CA
LinkedIn: linkedin.com/in/johndoe
GitHub: github.com/johndoe

PROFESSIONAL SUMMARY
Experienced Full-Stack Software Engineer with 5+ years of expertise in building scalable web applications. Proficient in Python, JavaScript, React, and cloud technologies. Strong background in API development, microservices architecture, and agile methodologies.

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, Java, SQL
Frameworks: FastAPI, Django, React, Node.js, Express
Databases: PostgreSQL, MongoDB, Redis, MySQL
Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, Kubernetes, CI/CD
Tools: Git, JIRA, Jenkins, Terraform

PROFESSIONAL EXPERIENCE

Senior Software Engineer | Tech Solutions Inc. | Jan 2021 - Present
- Led development of microservices architecture serving 1M+ daily active users
- Designed and implemented RESTful APIs using FastAPI and Python
- Reduced API response time by 40% through optimization and caching strategies
- Mentored junior developers and conducted code reviews
- Collaborated with product managers to define technical requirements

Software Engineer | Innovate Labs | Jun 2018 - Dec 2020
- Developed full-stack web applications using React and Django
- Implemented automated testing achieving 85% code coverage
- Integrated third-party APIs and payment gateways
- Participated in agile sprint planning and daily standups
- Optimized database queries reducing load time by 30%

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2014 - 2018
GPA: 3.7/4.0

PROJECTS
E-Commerce Platform
- Built a scalable e-commerce platform using microservices architecture
- Technologies: Python, FastAPI, React, PostgreSQL, Redis, AWS
- Implemented features: user authentication, product catalog, shopping cart, payment processing

Real-time Chat Application
- Developed a real-time chat application with WebSocket support
- Technologies: Node.js, Socket.io, MongoDB, React
- Features: private messaging, group chats, file sharing

CERTIFICATIONS
- AWS Certified Solutions Architect - Associate
- Professional Scrum Master (PSM I)

ACHIEVEMENTS
- Increased system performance by 60% through architectural improvements
- Successfully delivered 15+ projects on time and within budget
- Received "Employee of the Year" award in 2022
```

## Using the Sample Resume

### Method 1: Create a text file

```bash
# Create the file
cat > sample_resume.txt << 'EOF'
[Paste the resume content above]
EOF
```

### Method 2: Use the API with the sample text

```python
import requests

# Read the sample resume
with open('sample_resume.txt', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/upload-resume', files=files)
    print(response.json())
```

### Method 3: Test with cURL

```bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_resume.txt"
```

## Expected Results

When you upload this resume, the API should:

1. Extract the text successfully
2. Generate a summary like:
   - "Experienced Full-Stack Software Engineer with 5+ years of expertise in building scalable web applications using Python, JavaScript, and cloud technologies."

3. Suggest roles like:
   - "Senior Software Engineer"
   - "Full-Stack Developer"
   - "Backend Engineer"

4. When generating questions, you'll get role-specific MCQs such as:
   - Questions about Python/FastAPI for backend roles
   - Questions about React for frontend roles
   - Questions about AWS and DevOps for cloud roles
   - System design questions for senior positions

## Creating Your Own Test Resumes

You can create test resumes for different roles:

### Product Manager Resume
- Focus on: product strategy, roadmap planning, stakeholder management
- Skills: Agile, JIRA, analytics, user research

### Data Scientist Resume
- Focus on: machine learning, statistical analysis, data visualization
- Skills: Python, R, TensorFlow, scikit-learn, pandas

### DevOps Engineer Resume
- Focus on: CI/CD, infrastructure automation, monitoring
- Skills: Kubernetes, Docker, Terraform, Jenkins, AWS

## File Formats Supported

The API supports:
- `.txt` - Plain text files
- `.pdf` - PDF documents
- `.doc` - Microsoft Word documents (older format)
- `.docx` - Microsoft Word documents (newer format)

## Tips for Testing

1. **Test different difficulty levels**: Try 'easy', 'medium', and 'hard' when generating questions
2. **Test different roles**: Use various role names to see how questions adapt
3. **Test batch processing**: Generate multiple batches of questions for the same session
4. **Test error cases**: Try uploading unsupported file types or very large files
5. **Test with real resumes**: Use your own resume to get personalized questions!
