import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import List, Dict

class EmailService:
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("GMAIL_EMAIL")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD")
    
    async def send_job_matches_email(self, recipient_email: str, matched_jobs: List[Dict]):
        """Send email with matched jobs"""
        if not self.sender_email or not self.sender_password:
            raise Exception("Gmail credentials not configured in .env file")
        
        # Create HTML email
        html_content = self._create_email_html(matched_jobs)
        
        message = MIMEMultipart("alternative")
        message["Subject"] = f"🎯 {len(matched_jobs)} Job Matches Found for You!"
        message["From"] = self.sender_email
        message["To"] = recipient_email
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        try:
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                start_tls=True,
                username=self.sender_email,
                password=self.sender_password,
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
    
    def _create_email_html(self, matched_jobs: List[Dict]) -> str:
        """Create HTML content for email"""
        jobs_html = ""
        for idx, job in enumerate(matched_jobs, 1):
            jobs_html += f"""
            <div style="background: #f9fafb; border-left: 4px solid #3b82f6; padding: 20px; margin-bottom: 20px; border-radius: 8px;">
                <h3 style="color: #1f2937; margin: 0 0 10px 0;">{idx}. {job['title']}</h3>
                <p style="color: #6b7280; margin: 5px 0;"><strong>Company:</strong> {job['company']}</p>
                <p style="color: #6b7280; margin: 5px 0;"><strong>Location:</strong> {job.get('location', 'Not specified')}</p>
                <p style="color: #6b7280; margin: 5px 0;"><strong>Source:</strong> {job['source'].title()}</p>
                <p style="color: #10b981; margin: 5px 0;"><strong>Match Score:</strong> {job.get('match_score', 0):.0f}%</p>
                <p style="color: #4b5563; margin: 10px 0;"><strong>Why it matches:</strong> {job.get('match_reason', 'Good fit based on your profile')}</p>
                <a href="{job['url']}" style="display: inline-block; background: #3b82f6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; margin-top: 10px;">View Job</a>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Job Matches</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px;">
                <h1 style="color: white; margin: 0;">🎯 Your Job Matches Are Here!</h1>
                <p style="color: #e0e7ff; margin: 10px 0 0 0;">We found {len(matched_jobs)} jobs matching your profile in the last 24 hours</p>
            </div>
            
            {jobs_html}
            
            <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin-top: 30px; text-align: center;">
                <p style="color: #6b7280; margin: 0;">This email was sent by Job Matcher AI</p>
                <p style="color: #9ca3af; font-size: 14px; margin: 10px 0 0 0;">Automated job matching powered by AI</p>
            </div>
        </body>
        </html>
        """