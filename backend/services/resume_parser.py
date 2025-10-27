import PyPDF2
import io
import base64
from typing import Dict, List
import os
import google.generativeai as genai
import json

class ResumeParser:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def parse_pdf(self, base64_content: str) -> str:
        """Extract text from base64 encoded PDF"""
        try:
            pdf_bytes = base64.b64decode(base64_content)
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    async def extract_skills_and_experience(self, resume_text: str) -> Dict:
        """Use Gemini to extract skills and experience from resume"""
        try:
            prompt = f"""Extract the following from this resume and return ONLY valid JSON:
1. List of technical skills (programming languages, frameworks, tools)
2. Years of experience (estimate if not explicitly stated)
3. Key expertise areas

Resume:
{resume_text}

Return as JSON with keys: skills (array), experience (string), expertise (array)
Example: {{"skills": ["Python", "React"], "experience": "5 years", "expertise": ["Web Development"]}}"""

            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            result_text = response.text.strip()
            
            # Try to find JSON in the response
            if result_text.startswith('```json'):
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif result_text.startswith('```'):
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(result_text)
            return result
        except Exception as e:
            print(f"Error parsing resume with Gemini: {str(e)}")
            # Fallback to basic parsing if Gemini fails
            return {
                "skills": [],
                "experience": "Not specified",
                "expertise": []
            }