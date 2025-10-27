import PyPDF2
import io
import base64
from typing import Dict, List
import os
from openai import OpenAI

class ResumeParser:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
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
        """Use GPT-4o to extract skills and experience from resume"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert resume parser. Extract key information from resumes in JSON format."},
                    {"role": "user", "content": f"""Extract the following from this resume:
1. List of technical skills (programming languages, frameworks, tools)
2. Years of experience (estimate if not explicitly stated)
3. Key expertise areas

Resume:
{resume_text}

Return as JSON with keys: skills (array), experience (string), expertise (array)"""}
                ],
                temperature=0.3
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            # Fallback to basic parsing if OpenAI fails
            return {
                "skills": [],
                "experience": "Not specified",
                "expertise": []
            }