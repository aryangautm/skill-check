import google.generativeai as genai
from app.core.config import get_settings
from typing import Tuple, List, Dict
import json

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key)


class ResumeAnalyzer:
    """Service for analyzing resumes using Gemini 2.5 Flash."""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def analyze_resume(self, resume_text: str) -> Tuple[str, str]:
        """
        Analyze resume and return summary and suggested role.
        
        Args:
            resume_text: The extracted text from the resume
            
        Returns:
            Tuple of (summary, suggested_role)
        """
        prompt = f"""
        Analyze the following resume and provide:
        1. A concise summary (2-3 sentences) of the candidate's experience and skills
        2. A suggested role that best fits their career profile (e.g., "Software Engineer", "Product Manager", "Data Scientist")
        
        Resume:
        {resume_text}
        
        Return your response in JSON format:
        {{
            "summary": "...",
            "suggested_role": "..."
        }}
        """
        
        response = self.model.generate_content(prompt)
        result = json.loads(response.text)
        
        return result["summary"], result["suggested_role"]


class QuestionGenerator:
    """Service for generating MCQ questions using Gemini 2.5 Pro."""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
    
    def generate_questions(
        self, 
        resume_text: str, 
        role: str, 
        difficulty: str, 
        batch_size: int = 3
    ) -> List[Dict]:
        """
        Generate MCQ questions based on resume, role, and difficulty.
        
        Args:
            resume_text: The candidate's resume text
            role: The selected role
            difficulty: The difficulty level (easy, medium, hard)
            batch_size: Number of questions to generate (default: 3)
            
        Returns:
            List of question dictionaries
        """
        prompt = f"""
        Generate {batch_size} multiple-choice questions for a {role} position at {difficulty} difficulty level.
        Base the questions on the candidate's experience and the role requirements.
        
        Candidate's Resume:
        {resume_text}
        
        Role: {role}
        Difficulty: {difficulty}
        
        For each question:
        - Create a relevant technical or behavioral question
        - Provide 4 options (A, B, C, D)
        - Indicate the correct answer
        - Provide a brief explanation
        
        Return your response in JSON format as a list:
        [
            {{
                "question_text": "...",
                "options": [
                    {{"label": "A", "option": "..."}},
                    {{"label": "B", "option": "..."}},
                    {{"label": "C", "option": "..."}},
                    {{"label": "D", "option": "..."}}
                ],
                "correct_answer": "A",
                "explanation": "..."
            }}
        ]
        """
        
        response = self.model.generate_content(prompt)
        # Extract JSON from response, handling potential markdown formatting
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        questions = json.loads(text.strip())
        return questions
