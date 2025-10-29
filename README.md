# Job Matcher AI - n8n-Style Workflow Automation System

> A sophisticated workflow automation platform inspired by n8n, built from scratch using **React Flow** for visual workflow orchestration, **LangGraph** for state management, and **Google Gemini AI** for intelligent job matching.

## 🎯 What Makes This Special?

This is **not just another job board scraper** - it's a fully-functional **workflow automation engine** similar to n8n/Zapier, specifically designed for AI-powered job matching. The system demonstrates advanced skills in:

- **Visual Workflow Builder**: Interactive node-based canvas using React Flow
- **State Management**: LangGraph orchestrates complex multi-step workflows
- **AI Integration**: Google Gemini 2.0 for resume parsing and intelligent matching
- **Parallel Processing**: Asynchronous job fetching from 8+ sources simultaneously
- **Event-Driven Architecture**: Node-to-node data flow with real-time status updates

## 🌟 Key Features

### 🔄 Visual Workflow Engine
- **Interactive Canvas**: Drag-and-drop node visualization with React Flow
- **Real-time Execution**: Watch workflow progress as nodes change status
- **Connected Pipeline**: Visual edges show data flow between workflow nodes
- **State Tracking**: Each node maintains its execution state (pending → running → completed)

### 🤖 AI-Powered Intelligence
- **Resume Parser Node**: Gemini 2.0 extracts skills, experience, and expertise
- **Job Matcher Node**: AI scoring (0-100) with detailed reasoning
- **Smart Filtering**: Only surfaces 60%+ matches to reduce noise
- **Batch Processing**: Efficiently processes jobs in batches for optimal performance

### 🔍 Multi-Source Job Aggregation
- **8 Job Board Scrapers**: LinkedIn, Indeed, Glassdoor, Y Combinator, Wellfound, Jobrights.ai, Startups.gallery, Brian's Job Search
- **Parallel Execution**: Fetches from all sources simultaneously using async/await
- **24-Hour Window**: Only retrieves recently posted jobs
- **Deduplication**: Handles duplicate jobs across platforms

### 📧 Automated Notifications
- **Beautiful HTML Emails**: Professional job match cards with styling
- **Match Score Display**: Visual indicators for fit percentage
- **Direct Application Links**: One-click access to job postings
- **Personalized Reasoning**: AI explains why each job matches your profile

### 💾 Full Data Persistence
- **MongoDB Collections**: Resumes, jobs, matches, workflow executions
- **Execution History**: Track all workflow runs with timestamps
- **Match Archive**: Store AI-generated scores and reasoning
- **Query API**: Retrieve past matches and execution logs

## 🏗️ Architecture

### Tech Stack
- **Frontend**: React 19, React Flow (workflow visualization), Tailwind CSS, Shadcn UI
- **Backend**: FastAPI (async Python), LangChain, LangGraph (workflow orchestration)
- **AI Engine**: Google Gemini 2.0 Flash
- **Database**: MongoDB (document store for workflow state)
- **Email**: Gmail SMTP (aiosmtplib)
- **Job Scrapers**: BeautifulSoup4, aiohttp (async scraping)

## 🚀 Local Setup Guide for Visual Studio Code

### **Prerequisites**

Before starting, make sure you have these installed:

1. **Node.js** (v18 or higher)
   - Download: https://nodejs.org/
   - Check: `node --version`

2. **Python** (3.11 or higher)
   - Download: https://www.python.org/downloads/
   - Check: `python --version` or `python3 --version`

3. **MongoDB**
   - Download: https://www.mongodb.com/try/download/community
   - Or use Docker: `docker run -d -p 27017:27017 --name mongodb mongo`

4. **Git** (to clone the repo)
   - Download: https://git-scm.com/

---

## 📦 Step-by-Step Setup

### **Step 1: Clone the Repository**

```bash
# Open terminal in VS Code (Ctrl+` or Cmd+`)
git clone <your-github-repo-url>
cd <project-folder-name>

# Open in VS Code
code .
```

### **Step 2: Backend Setup**

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy the content below or use: cp .env.example .env
```

**Create `/backend/.env` file:**
```bash
MONGO_URL="mongodb://localhost:27017"
DB_NAME="job_matcher_db"
CORS_ORIGINS="*"

# Google Gemini API Key - Get from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY="your-gemini-api-key-here"

# Gmail SMTP Configuration
GMAIL_EMAIL="your-email@gmail.com"
GMAIL_APP_PASSWORD="your-16-char-app-password"

# JWT Secret - Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET="your-secret-key-here"

# LangSmith (Optional)
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT="job-matcher"
```

### **Step 3: Frontend Setup**

```bash
# Open a NEW terminal (Ctrl+Shift+` or Cmd+Shift+`)
cd frontend

# Install dependencies (using yarn or npm)
yarn install
# OR
npm install

# Create .env file
```

**Create `/frontend/.env` file:**
```bash
# Backend URL (for local development)
REACT_APP_BACKEND_URL="http://localhost:8001"
```

### **Step 4: Start MongoDB**

```bash
# Option 1: If MongoDB is installed locally
mongod

# Option 2: If using Docker
docker run -d -p 27017:27017 --name mongodb mongo

# Option 3: If MongoDB is already running, skip this step
```

### **Step 5: Start Backend Server**

```bash
# In backend terminal (make sure venv is activated)
cd backend
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

### **Step 6: Start Frontend**

```bash
# In frontend terminal
cd frontend
yarn start
# OR
npm start
```

Browser should automatically open at: **http://localhost:3000**

---

## 🔧 VS Code Configuration (Optional but Recommended)

### **Install VS Code Extensions:**

1. **Python** (by Microsoft)
2. **Pylance** (Python IntelliSense)
3. **ESLint** (JavaScript linting)
4. **Prettier** (Code formatting)
5. **MongoDB for VS Code** (MongoDB viewer)
6. **Thunder Client** (API testing - alternative to Postman)

### **Create `.vscode/launch.json` for Debugging:**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "server:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8001"
      ],
      "jinja": true,
      "justMyCode": true,
      "cwd": "${workspaceFolder}/backend"
    },
    {
      "name": "Chrome: React",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

## 🧪 Testing the App

1. **Upload Resume:**
   - Enter your email
   - Paste resume text or upload PDF
   - Click "Upload Resume"

2. **Run Workflow:**
   - Click "Run Job Matcher"
   - Watch workflow visualization update
   - Wait 2-5 minutes

3. **Check Results:**
   - Email will be sent to your Gmail
   - Or view results in UI

---

## 📝 Quick Commands Reference

```bash
# Start backend (in backend folder)
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Start frontend (in frontend folder)
yarn start  # or npm start

# Start MongoDB (Docker)
docker run -d -p 27017:27017 --name mongodb mongo

# View backend logs
# (Check terminal where backend is running)

# Install new Python package
pip install <package-name>
pip freeze > requirements.txt

# Install new npm package
yarn add <package-name>  # or npm install <package-name>
```

---

### Workflow Architecture (LangGraph State Machine)

This system implements a **directed acyclic graph (DAG)** workflow engine using LangGraph:

```
START
  ↓
┌─────────────────────┐
│  Upload Resume      │  ← User Input
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Parse Resume       │  ← Gemini AI Node
│  (Extract Skills)   │
└──────────┬──────────┘
           ↓
     ┌─────┴─────┐
     ↓           ↓
┌─────────┐  ┌─────────┐
│ Fetch   │  │ Fetch   │  ← Parallel Execution
│ Jobs    │  │ More    │
│ (8 src) │  │ Jobs    │
└────┬────┘  └────┬────┘
     └─────┬─────┘
           ↓
┌─────────────────────┐
│  Match Jobs         │  ← Gemini AI Node
│  (Score 0-100)      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Send Email         │  ← Output Node
└──────────┬──────────┘
           ↓
          END
```

### LangGraph Workflow Implementation

Each workflow node is an **async Python function** that:
1. Receives the current state (TypedDict)
2. Performs its operation (parse, fetch, match, send)
3. Updates and returns the modified state
4. Passes state to the next node(s)

**State Management**:
```python
class WorkflowState(TypedDict):
    user_id: str
    resume_data: Dict
    job_sources: List[str]
    all_jobs: List[Dict]
    matched_jobs: List[Dict]
    status: str
    error: str
```

**Parallel Node Execution**:
The "Fetch Jobs" node spawns 8 async tasks simultaneously, collecting results from all job boards in parallel before proceeding to matching.

### React Flow Visualization

The frontend uses **React Flow** to create an interactive, n8n-style workflow canvas:

**Features**:
- **Custom Node Components**: Each workflow step is a styled React component with icon, title, description, and status indicator
- **Dynamic Edge Rendering**: Blue animated connections between nodes show data flow
- **Real-time State Updates**: Nodes change color based on execution status:
  - Gray (Pending) → Blue (Running) → Green (Completed) → Red (Failed)
- **Handle Components**: Connection points (source/target) enable visual data flow representation
- **Smooth Transitions**: SmoothStep edges with arrow markers for professional appearance
- **Responsive Canvas**: Pan, zoom, and fit controls for easy navigation

**Implementation Highlights**:
```jsx
// Custom Workflow Node
const WorkflowNode = ({ data }) => (
  <div className="workflow-node">
    <Handle type="target" position={Position.Top} />
    <Icon component={data.icon} />
    <Title>{data.label}</Title>
    <Status>{data.status}</Status>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

// React Flow with live state
<ReactFlow
  nodes={nodes}
  edges={edges}
  nodeTypes={{ workflow: WorkflowNode }}
  fitView
/>
```

## 🚀 Setup Instructions

### Prerequisites
- MongoDB running on localhost:27017
- Google Gemini API key
- Gmail account with App Password

### 1. Backend Configuration

Edit `/app/backend/.env` with your credentials:

```bash
# MongoDB
MONGO_URL="mongodb://localhost:27017"
DB_NAME="job_matcher_db"
CORS_ORIGINS="*"

# Google Gemini API Key - REQUIRED
GEMINI_API_KEY="your-gemini-api-key-here"

# Gmail SMTP - REQUIRED
GMAIL_EMAIL="your.email@gmail.com"
GMAIL_APP_PASSWORD="your-16-char-app-password"

# JWT Secret
JWT_SECRET="your-secret-key-for-jwt-tokens"

# LangSmith (Optional - for workflow debugging)
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT="job-matcher"
```

#### How to Get Gemini API Key:
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)

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

### Workflow Execution
The core workflow automation API:

```bash
# Execute complete workflow (main automation endpoint)
POST /api/workflow/execute?user_email={email}
Body: {
  "resume_id": "uuid",
  "job_sources": ["linkedin", "indeed", "glassdoor", ...],
  "send_email": true
}
Response: {
  "execution_id": "uuid",
  "status": "completed",
  "jobs_found": 45,
  "jobs_matched": 12,
  "matched_jobs": [...]
}

# Get workflow execution status (poll for progress)
GET /api/workflow/execution/{execution_id}
Response: {
  "status": "running",
  "jobs_found": 18,
  "jobs_matched": 0,
  "started_at": "2025-01-01T12:00:00Z"
}
```

### Resume Management
```bash
# Upload resume (workflow input)
POST /api/resume/upload
Content-Type: multipart/form-data
Body: { user_email, resume_text OR file }
Response: Resume object with ID

# Get resume by ID
GET /api/resume/{resume_id}

# Get user's resumes
GET /api/resume/user/{user_email}
```

### Job Matches
```bash
# Get job matches (workflow output)
GET /api/jobs/matches/{user_email}?limit=50
Response: [
  {
    "job_id": "linkedin_123",
    "title": "Senior Software Engineer",
    "company": "Tech Corp",
    "match_score": 85,
    "match_reason": "Strong Python and React skills...",
    "url": "https://...",
    "matched_at": "2025-01-01T12:30:00Z"
  },
  ...
]
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

**1. Gemini API Error**
```bash
# Check if key is set
cat /app/backend/.env | grep GEMINI_API_KEY
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

- [ ] **Drag-and-Drop Workflow Builder**: User-customizable node placement
- [ ] **Custom Node Creation**: Allow users to add new job sources or processing steps
- [ ] **Conditional Branching**: If-else logic in workflow paths
- [ ] **Scheduled Executions**: Cron-based automatic daily runs
- [ ] **Cover Letter Generation**: AI-powered custom cover letters per job
- [ ] **Google Sheets Integration**: Auto-export matches to spreadsheet
- [ ] **Webhook Triggers**: Start workflow from external events
- [ ] **Job Application Automation**: Auto-apply via APIs where available
- [ ] **Multi-Resume Profiles**: Different resumes for different job types
- [ ] **Analytics Dashboard**: Execution history, success rates, trends

## 💼 Technical Highlights (For Portfolio/Resume)

This project demonstrates proficiency in:

### **Frontend Engineering**
- React 19 with hooks (useState, useMemo, useCallback)
- React Flow for complex interactive visualizations
- Tailwind CSS + Shadcn UI component library
- Responsive design and modern UX patterns
- Real-time state management and updates

### **Backend Development**
- FastAPI async Python (modern async/await patterns)
- MongoDB with Motor (async MongoDB driver)
- RESTful API design with proper HTTP methods
- File upload handling (multipart/form-data)
- Error handling and validation

### **AI/ML Integration**
- Google Gemini AI API integration
- Prompt engineering for structured outputs
- JSON parsing from LLM responses
- Batch processing for cost optimization
- Fallback strategies for reliability

### **Workflow Orchestration**
- LangGraph state machines
- Directed Acyclic Graph (DAG) implementation
- Parallel async execution
- State persistence across workflow steps
- Node-based architecture

### **DevOps & Architecture**
- Docker containerization
- MongoDB database design
- Environment variable management
- Email SMTP integration (aiosmtplib)
- Web scraping at scale (BeautifulSoup4, aiohttp)
- Logging and monitoring

### **Software Engineering Best Practices**
- Modular code organization (services, models, routes)
- Type hints and Pydantic models
- Async/await for I/O-bound operations
- Error handling and graceful degradation
- Documentation (README, API docs)

## 🤝 Contributing

This is a template project. Feel free to fork and customize for your needs!

## 📄 License

MIT License - feel free to use for personal or commercial projects.
