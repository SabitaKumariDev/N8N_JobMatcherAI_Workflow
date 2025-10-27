from typing import List, Dict
import os
import google.generativeai as genai
import json

class JobMatcher:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def match_jobs(self, resume_data: Dict, jobs: List[Dict]) -> List[Dict]:
        """Match jobs against resume using Gemini"""
        if not jobs:
            return []
        
        matched_jobs = []
        
        # Process jobs in batches of 5 for efficiency
        batch_size = 5
        for i in range(0, len(jobs), batch_size):
            batch = jobs[i:i+batch_size]
            matches = await self._match_batch(resume_data, batch)
            matched_jobs.extend(matches)
        
        # Sort by match score and return top matches
        matched_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        return [job for job in matched_jobs if job.get('match_score', 0) >= 60]  # Only return 60%+ matches
    
    async def _match_batch(self, resume_data: Dict, jobs: List[Dict]) -> List[Dict]:
        """Match a batch of jobs"""
        try:
            jobs_text = "\n\n".join([
                f"Job {idx+1}:\nTitle: {job['title']}\nCompany: {job['company']}\nDescription: {job['description'][:500]}..."
                for idx, job in enumerate(jobs)
            ])
            
            prompt = f"""You are an expert job matcher. Analyze these jobs against the candidate's profile and provide match scores.

Candidate Profile:
- Skills: {', '.join(resume_data.get('skills', []))}
- Experience: {resume_data.get('experience', 'Not specified')}
- Expertise: {', '.join(resume_data.get('expertise', []))}

Jobs to evaluate:
{jobs_text}

For each job, provide:
1. Match score (0-100) based on skills, experience, and fit
2. Brief reason for the match score (1-2 sentences)

Return ONLY valid JSON array: [{{"job_index": 0, "match_score": 85, "match_reason": "..."}}]
"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from response
            if result_text.startswith('```json'):
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif result_text.startswith('```'):
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            matches = json.loads(result_text)
            
            # Merge match results with original job data
            result = []
            for match in matches:
                job_idx = match['job_index']
                if 0 <= job_idx < len(jobs):
                    job_copy = jobs[job_idx].copy()
                    job_copy['match_score'] = match['match_score']
                    job_copy['match_reason'] = match['match_reason']
                    result.append(job_copy)
            
            return result
        except Exception as e:
            print(f"Error matching jobs with Gemini: {str(e)}")
            # Return jobs with default scores on error
            return [{'match_score': 50, 'match_reason': 'Unable to calculate precise match', **job} for job in jobs]