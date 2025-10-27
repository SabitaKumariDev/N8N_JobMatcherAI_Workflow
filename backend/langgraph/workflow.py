from typing import TypedDict, Annotated, List, Dict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import asyncio

class WorkflowState(TypedDict):
    """State passed between workflow nodes"""
    user_id: str
    resume_id: str
    resume_data: Dict
    job_sources: List[str]
    all_jobs: List[Dict]
    matched_jobs: List[Dict]
    send_email: bool
    user_email: str
    status: str
    error: str

class JobMatcherWorkflow:
    def __init__(self, db, resume_parser, job_matcher, email_service, job_fetchers):
        self.db = db
        self.resume_parser = resume_parser
        self.job_matcher = job_matcher
        self.email_service = email_service
        self.job_fetchers = job_fetchers
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("fetch_resume", self.fetch_resume_node)
        workflow.add_node("parse_resume", self.parse_resume_node)
        workflow.add_node("fetch_jobs", self.fetch_jobs_node)
        workflow.add_node("match_jobs", self.match_jobs_node)
        workflow.add_node("send_email", self.send_email_node)
        
        # Define edges
        workflow.add_edge(START, "fetch_resume")
        workflow.add_edge("fetch_resume", "parse_resume")
        workflow.add_edge("parse_resume", "fetch_jobs")
        workflow.add_edge("fetch_jobs", "match_jobs")
        workflow.add_edge("match_jobs", "send_email")
        workflow.add_edge("send_email", END)
        
        return workflow.compile()
    
    async def fetch_resume_node(self, state: WorkflowState) -> WorkflowState:
        """Fetch resume from database"""
        try:
            resume = await self.db.resumes.find_one({"id": state["resume_id"]}, {"_id": 0})
            if not resume:
                state["error"] = "Resume not found"
                state["status"] = "failed"
                return state
            
            state["resume_data"] = resume
            state["status"] = "resume_fetched"
            return state
        except Exception as e:
            state["error"] = f"Error fetching resume: {str(e)}"
            state["status"] = "failed"
            return state
    
    async def parse_resume_node(self, state: WorkflowState) -> WorkflowState:
        """Parse resume and extract skills"""
        try:
            resume_text = state["resume_data"].get("resume_text", "")
            
            # Check if already parsed
            if state["resume_data"].get("parsed_skills"):
                state["status"] = "resume_parsed"
                return state
            
            # Parse using GPT-4o
            parsed_data = await self.resume_parser.extract_skills_and_experience(resume_text)
            
            # Update resume in state and database
            state["resume_data"]["parsed_skills"] = parsed_data.get("skills", [])
            state["resume_data"]["parsed_experience"] = parsed_data.get("experience", "")
            state["resume_data"]["expertise"] = parsed_data.get("expertise", [])
            
            await self.db.resumes.update_one(
                {"id": state["resume_id"]},
                {"$set": {
                    "parsed_skills": parsed_data.get("skills", []),
                    "parsed_experience": parsed_data.get("experience", ""),
                    "expertise": parsed_data.get("expertise", [])
                }}
            )
            
            state["status"] = "resume_parsed"
            return state
        except Exception as e:
            state["error"] = f"Error parsing resume: {str(e)}"
            state["status"] = "failed"
            return state
    
    async def fetch_jobs_node(self, state: WorkflowState) -> WorkflowState:
        """Fetch jobs from all sources in parallel"""
        try:
            all_jobs = []
            tasks = []
            
            # Create keywords from resume skills
            keywords = " ".join(state["resume_data"].get("parsed_skills", [])[:3])  # Top 3 skills
            if not keywords:
                keywords = "software engineer"
            
            # Fetch from each source
            for source in state["job_sources"]:
                if source in self.job_fetchers:
                    tasks.append(self.job_fetchers[source].fetch_jobs(keywords=keywords, limit=15))
            
            # Execute all fetchers in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Collect all jobs
            for result in results:
                if isinstance(result, list):
                    all_jobs.extend(result)
            
            state["all_jobs"] = all_jobs
            state["status"] = "jobs_fetched"
            return state
        except Exception as e:
            state["error"] = f"Error fetching jobs: {str(e)}"
            state["status"] = "failed"
            return state
    
    async def match_jobs_node(self, state: WorkflowState) -> WorkflowState:
        """Match jobs using GPT-4o"""
        try:
            resume_data = {
                "skills": state["resume_data"].get("parsed_skills", []),
                "experience": state["resume_data"].get("parsed_experience", ""),
                "expertise": state["resume_data"].get("expertise", [])
            }
            
            matched_jobs = await self.job_matcher.match_jobs(resume_data, state["all_jobs"])
            
            state["matched_jobs"] = matched_jobs
            state["status"] = "jobs_matched"
            return state
        except Exception as e:
            state["error"] = f"Error matching jobs: {str(e)}"
            state["status"] = "failed"
            return state
    
    async def send_email_node(self, state: WorkflowState) -> WorkflowState:
        """Send email with matched jobs"""
        try:
            if not state.get("send_email") or not state.get("matched_jobs"):
                state["status"] = "completed_no_email"
                return state
            
            user_email = state.get("user_email")
            if not user_email:
                state["error"] = "User email not provided"
                state["status"] = "failed"
                return state
            
            await self.email_service.send_job_matches_email(user_email, state["matched_jobs"])
            
            state["status"] = "completed"
            return state
        except Exception as e:
            state["error"] = f"Error sending email: {str(e)}"
            state["status"] = "failed"
            return state
    
    async def run(self, initial_state: Dict) -> Dict:
        """Run the workflow"""
        try:
            result = await self.graph.ainvoke(initial_state)
            return result
        except Exception as e:
            return {
                **initial_state,
                "status": "failed",
                "error": str(e)
            }