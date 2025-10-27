from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from typing import Optional, List
from pydantic import BaseModel
import base64

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Import models
from models.resume import Resume, ResumeCreate
from models.job import Job, JobMatch
from models.workflow import WorkflowExecution, WorkflowRequest

# Import services
from services.resume_parser import ResumeParser
from services.job_matcher import JobMatcher
from services.email_service import EmailService

# Import job fetchers
from services.job_fetchers.linkedin import LinkedInScraper
from services.job_fetchers.indeed import IndeedScraper
from services.job_fetchers.jobrights import JobrightsScraper
from services.job_fetchers.startups_gallery import StartupsGalleryScraper
from services.job_fetchers.briansjobs import BriansJobsScraper
from services.job_fetchers.glassdoor import GlassdoorScraper
from services.job_fetchers.ycombinator import YCombinatorScraper
from services.job_fetchers.wellfound import WellfoundScraper

# Import workflow
from langgraph.workflow import JobMatcherWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
resume_parser = ResumeParser()
job_matcher = JobMatcher()
email_service = EmailService()

# Initialize job fetchers
job_fetchers = {
    "linkedin": LinkedInScraper(),
    "indeed": IndeedScraper(),
    "jobrights": JobrightsScraper(),
    "startups_gallery": StartupsGalleryScraper(),
    "briansjobs": BriansJobsScraper(),
    "glassdoor": GlassdoorScraper(),
    "ycombinator": YCombinatorScraper(),
    "wellfound": WellfoundScraper()
}

# Initialize workflow
workflow = JobMatcherWorkflow(db, resume_parser, job_matcher, email_service, job_fetchers)

# Create the main app without a prefix
app = FastAPI(title="Job Matcher AI", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ===== API Endpoints =====

@api_router.get("/")
async def root():
    return {"message": "Job Matcher AI API", "version": "1.0.0"}


@api_router.post("/resume/upload", response_model=Resume)
async def upload_resume(
    user_email: str = Form(...),
    resume_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """Upload resume (text or PDF)"""
    try:
        final_resume_text = ""
        file_type = "text"
        file_name = None
        
        # Handle file upload
        if file:
            file_name = file.filename
            if file.filename.endswith('.pdf'):
                file_type = "pdf"
                content = await file.read()
                base64_content = base64.b64encode(content).decode('utf-8')
                final_resume_text = resume_parser.parse_pdf(base64_content)
            else:
                # Assume text file
                final_resume_text = (await file.read()).decode('utf-8')
        elif resume_text:
            final_resume_text = resume_text
        else:
            raise HTTPException(status_code=400, detail="Either resume_text or file must be provided")
        
        # Create resume object
        resume = Resume(
            user_id=user_email,
            resume_text=final_resume_text,
            file_name=file_name,
            file_type=file_type
        )
        
        # Store in database
        resume_dict = resume.model_dump()
        resume_dict['uploaded_at'] = resume_dict['uploaded_at'].isoformat()
        
        await db.resumes.insert_one(resume_dict)
        
        logger.info(f"Resume uploaded for user: {user_email}")
        return resume
        
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/resume/{resume_id}", response_model=Resume)
async def get_resume(resume_id: str):
    """Get resume by ID"""
    resume = await db.resumes.find_one({"id": resume_id}, {"_id": 0})
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Convert ISO string back to datetime if needed
    from datetime import datetime
    if isinstance(resume.get('uploaded_at'), str):
        resume['uploaded_at'] = datetime.fromisoformat(resume['uploaded_at'])
    
    return Resume(**resume)


@api_router.get("/resume/user/{user_email}")
async def get_user_resumes(user_email: str):
    """Get all resumes for a user"""
    resumes = await db.resumes.find({"user_id": user_email}, {"_id": 0}).to_list(100)
    
    # Convert datetime fields
    from datetime import datetime
    for resume in resumes:
        if isinstance(resume.get('uploaded_at'), str):
            resume['uploaded_at'] = datetime.fromisoformat(resume['uploaded_at'])
    
    return resumes


@api_router.post("/workflow/execute")
async def execute_workflow(request: WorkflowRequest, user_email: str):
    """Execute job matching workflow"""
    try:
        # Validate resume exists
        resume = await db.resumes.find_one({"id": request.resume_id}, {"_id": 0})
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Create workflow execution record
        execution = WorkflowExecution(
            user_id=user_email,
            workflow_config=request.model_dump(),
            status="running"
        )
        
        execution_dict = execution.model_dump()
        execution_dict['started_at'] = execution_dict['started_at'].isoformat()
        await db.workflow_executions.insert_one(execution_dict)
        
        # Prepare initial state
        initial_state = {
            "user_id": user_email,
            "resume_id": request.resume_id,
            "resume_data": {},
            "job_sources": request.job_sources,
            "all_jobs": [],
            "matched_jobs": [],
            "send_email": request.send_email,
            "user_email": user_email,
            "status": "started",
            "error": ""
        }
        
        # Run workflow
        logger.info(f"Starting workflow for user: {user_email}")
        result = await workflow.run(initial_state)
        
        # Update execution record
        from datetime import datetime, timezone
        await db.workflow_executions.update_one(
            {"id": execution.id},
            {"$set": {
                "status": result["status"],
                "jobs_found": len(result.get("all_jobs", [])),
                "jobs_matched": len(result.get("matched_jobs", [])),
                "email_sent": result.get("status") == "completed",
                "error_message": result.get("error", ""),
                "completed_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        # Store matched jobs in database
        if result.get("matched_jobs"):
            for job in result["matched_jobs"]:
                job_match = JobMatch(
                    user_id=user_email,
                    job_id=job.get("job_id", "unknown"),
                    match_score=job.get("match_score", 0),
                    match_reason=job.get("match_reason", "")
                )
                job_match_dict = job_match.model_dump()
                job_match_dict['matched_at'] = job_match_dict['matched_at'].isoformat()
                await db.job_matches.insert_one(job_match_dict)
        
        logger.info(f"Workflow completed: {result['status']} - {len(result.get('matched_jobs', []))} jobs matched")
        
        return {
            "execution_id": execution.id,
            "status": result["status"],
            "jobs_found": len(result.get("all_jobs", [])),
            "jobs_matched": len(result.get("matched_jobs", [])),
            "matched_jobs": result.get("matched_jobs", []),
            "error": result.get("error", "")
        }
        
    except Exception as e:
        logger.error(f"Error executing workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/workflow/execution/{execution_id}")
async def get_workflow_execution(execution_id: str):
    """Get workflow execution status"""
    execution = await db.workflow_executions.find_one({"id": execution_id}, {"_id": 0})
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution


@api_router.get("/jobs/matches/{user_email}")
async def get_job_matches(user_email: str, limit: int = 50):
    """Get all job matches for a user"""
    matches = await db.job_matches.find({"user_id": user_email}, {"_id": 0}).sort("matched_at", -1).to_list(limit)
    return matches


@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "openai": "configured" if os.getenv("OPENAI_API_KEY") else "not_configured",
            "email": "configured" if os.getenv("GMAIL_APP_PASSWORD") else "not_configured"
        }
    }


# Include the router in the main app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()