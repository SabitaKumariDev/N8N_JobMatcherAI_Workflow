# Job Matcher AI - Automated Resume-to-Job Matching System

An intelligent job matching workflow built with **React Flow**, **FastAPI**, **LangChain**, **LangGraph**, and **Gemini API Key**. This system automatically fetches jobs from 8+ job boards posted in the last 24 hours, matches them against your resume using AI, and emails you the best matches.

## 🌟 Features

- **📄 Resume Upload**: Support for both PDF and text format
- **🧠 AI-Powered Parsing**: Extracts skills and experience using GPT-4o
- **🔍 Multi-Source Job Fetching**: Scrapes 8+ job boards (LinkedIn, Indeed, Glassdoor, Y Combinator, Wellfound, etc.)
- **🎯 Intelligent Matching**: Uses GPT-4o to match jobs with resume (60%+ match threshold)
- **📧 Email Notifications**: Automatically sends matched jobs to your email
- **🔄 Workflow Visualization**: Beautiful React Flow canvas showing the entire process
- **💾 MongoDB Storage**: Persists resumes, jobs, and match results

## 🏗️ Architecture

### Tech Stack
- **Frontend**: React 19, React Flow, Tailwind CSS, Shadcn UI
- **Backend**: FastAPI, Python 3.11
- **LLM Integration**: OpenAI GPT-4o
- **Workflow**: LangChain, LangGraph, LangSmith
- **Database**: MongoDB
- **Email**: Gmail SMTP (aiosmtplib)

### Workflow Steps

```
1. Upload Resume (PDF/Text)
   ↓
2. Parse Resume (GPT-4o extracts skills)
   ↓
3. Fetch Jobs (Parallel scraping from 8 sources)
   ↓
4. Match Jobs (AI scoring 0-100)
   ↓
5. Send Email (Top matches to user)
```

### Job Sources
- LinkedIn
- Indeed
- Jobrights.ai
- Startups.gallery
- Brian's Job Search
- Glassdoor
- Y Combinator Jobs
- Wellfound (AngelList)

## 🚀 Setup Instructions

### Prerequisites
- MongoDB running on localhost:27017
- OpenAI API key
- Gmail account with App Password

### 1. Backend Configuration

Edit `/app/backend/.env` with your credentials:

```bash
# MongoDB
MONGO_URL="mongodb://localhost:27017"
DB_NAME="job_matcher_db"
CORS_ORIGINS="*"

# OpenAI API Key - REQUIRED
OPENAI_API_KEY="sk-your-openai-api-key-here"

# Gmail SMTP - REQUIRED
GMAIL_EMAIL="sabita.softech@gmail.com"
GMAIL_APP_PASSWORD="your-16-char-app-password"

# JWT Secret
JWT_SECRET="your-secret-key-for-jwt-tokens"

# LangSmith (Optional)
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT="job-matcher"
```

#### How to Get Gmail App Password:
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Create a new app password for "Mail"
5. Copy the 16-character password (no spaces)

### 2. Start Services

Backend and frontend auto-start via Supervisor. If needed:

```bash
# Restart backend
sudo supervisorctl restart backend

# Restart frontend
sudo supervisorctl restart frontend

# Check status
sudo supervisorctl status
```

### 3. Access Application

- **Frontend**: https://resume-match-ai-4.preview.emergentagent.com
- **Backend API**: https://resume-match-ai-4.preview.emergentagent.com/api
- **API Docs**: https://resume-match-ai-4.preview.emergentagent.com/docs

## 📖 Usage

### Step 1: Upload Resume
1. Enter your email address
2. Choose between:
   - **Text**: Paste your resume text
   - **PDF**: Upload your resume PDF
3. Click "Upload Resume"

### Step 2: Run Workflow
1. Click "Run Job Matcher"
2. Watch the workflow visualization update in real-time
3. Wait for completion (usually 2-5 minutes)

### Step 3: View Results
- Check your email for matched jobs
- Or view results in the UI
- Each match includes:
  - Match score (0-100%)
  - Match reason (why it fits)
  - Job details & direct link

## 🔧 API Endpoints

### Resume Management
```bash
# Upload resume
POST /api/resume/upload
Content-Type: multipart/form-data
Body: { user_email, resume_text OR file }

# Get resume by ID
GET /api/resume/{resume_id}

# Get user's resumes
GET /api/resume/user/{user_email}
```

### Workflow Execution
```bash
# Execute job matching workflow
POST /api/workflow/execute?user_email={email}
Body: {
  "resume_id": "uuid",
  "job_sources": ["linkedin", "indeed", ...],
  "send_email": true
}

# Get execution status
GET /api/workflow/execution/{execution_id}

# Get job matches
GET /api/jobs/matches/{user_email}
```

### Health Check
```bash
GET /api/health
```

## 🗄️ Database Collections

### `resumes`
```javascript
{
  id: "uuid",
  user_id: "email",
  resume_text: "...",
  parsed_skills: ["Python", "React"],
  parsed_experience: "5 years",
  file_name: "resume.pdf",
  file_type: "pdf",
  uploaded_at: ISODate()
}
```

### `jobs`
```javascript
{
  id: "uuid",
  job_id: "linkedin_123",
  source: "linkedin",
  title: "Senior Software Engineer",
  company: "Tech Corp",
  description: "...",
  location: "Remote",
  url: "https://...",
  posted_date: ISODate(),
  scraped_at: ISODate()
}
```

### `job_matches`
```javascript
{
  id: "uuid",
  user_id: "email",
  job_id: "linkedin_123",
  match_score: 85.5,
  match_reason: "Strong match with Python, React skills",
  matched_at: ISODate()
}
```

### `workflow_executions`
```javascript
{
  id: "uuid",
  user_id: "email",
  workflow_config: {...},
  status: "completed",
  jobs_found: 45,
  jobs_matched: 12,
  email_sent: true,
  started_at: ISODate(),
  completed_at: ISODate()
}
```

## 🐛 Debugging

### Check Logs
```bash
# Backend logs
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/backend.out.log

# Frontend logs
tail -f /var/log/supervisor/frontend.err.log

# MongoDB logs
tail -f /var/log/mongodb/mongod.log
```

### Common Issues

**1. OpenAI API Error**
```bash
# Check if key is set
cat /app/backend/.env | grep OPENAI_API_KEY
```

**2. Email Not Sending**
```bash
# Verify Gmail credentials
# Make sure you're using App Password, not regular password
```

**3. Jobs Not Found**
```bash
# Some job sites may block scraping
# Check backend logs for specific scraper errors
```

## 📝 Notes

### Job Scraping Limitations
- LinkedIn and Indeed have rate limits and anti-scraping measures
- Some scrapers return mock data as placeholders
- In production, use official APIs or dedicated scraping services (like ScraperAPI, Bright Data)

### LangGraph Workflow
The workflow is built using LangGraph's StateGraph:
- Each node is an async Python function
- State is passed between nodes
- Supports parallel execution for job fetching
- Easy to extend with new nodes

### Extending the System

**Add New Job Source**:
1. Create scraper in `/app/backend/services/job_fetchers/{source}.py`
2. Add to `job_fetchers` dict in `server.py`
3. Include source name in workflow request

**Customize Matching Logic**:
Edit `/app/backend/services/job_matcher.py` to adjust:
- Match threshold (default 60%)
- Batch size for GPT-4o calls
- Scoring criteria

**Add Cover Letter Generation** (Future):
Create new LangGraph node that:
1. Takes matched job + resume
2. Uses GPT-4o to generate custom cover letter
3. Stores in MongoDB
4. Includes in email

## 🎯 Future Enhancements

- [ ] Job scoring with multiple LLM models
- [ ] Auto-apply to jobs via APIs
- [ ] Cover letter generation per job
- [ ] Google Sheets integration
- [ ] Scheduled daily runs
- [ ] User dashboard with analytics
- [ ] Job application tracking

## 🤝 Contributing

This is a template project. Feel free to fork and customize for your needs!

## 📄 License

MIT License - feel free to use for personal or commercial projects.

---

**Built with ❤️ using Emergent Agent Platform**
