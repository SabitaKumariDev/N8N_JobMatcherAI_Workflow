import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import WorkflowCanvas from '../components/WorkflowCanvas';
import ResumeUpload from '../components/ResumeUpload';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';
import { Play, FileText, Mail, Loader2 } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState('');
  const [resumeId, setResumeId] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [workflowStatus, setWorkflowStatus] = useState({});

  const handleResumeUpload = (uploadedResumeId, email) => {
    setResumeId(uploadedResumeId);
    setUserEmail(email);
    toast.success('Resume uploaded successfully!');
  };

  const handleExecuteWorkflow = async () => {
    if (!resumeId || !userEmail) {
      toast.error('Please upload your resume first');
      return;
    }

    setIsExecuting(true);
    setWorkflowStatus({ status: 'running' });

    try {
      const response = await axios.post(
        `${API}/workflow/execute?user_email=${encodeURIComponent(userEmail)}`,
        {
          resume_id: resumeId,
          job_sources: [
            'linkedin',
            'indeed',
            'jobrights',
            'startups_gallery',
            'briansjobs',
            'glassdoor',
            'ycombinator',
            'wellfound'
          ],
          send_email: true
        }
      );

      const result = response.data;
      setWorkflowStatus(result);

      if (result.status === 'completed') {
        toast.success(
          `✨ Found ${result.jobs_matched} matching jobs! Check your email.`
        );
        // Navigate to results after 2 seconds
        setTimeout(() => {
          navigate('/results', {
            state: {
              matchedJobs: result.matched_jobs,
              userEmail: userEmail
            }
          });
        }, 2000);
      } else if (result.error) {
        toast.error(`Workflow failed: ${result.error}`);
      }
    } catch (error) {
      console.error('Workflow execution error:', error);
      toast.error(
        error.response?.data?.detail || 'Failed to execute workflow'
      );
      setWorkflowStatus({ status: 'failed', error: error.message });
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Job Matcher AI
                </h1>
                <p className="text-sm text-gray-600">
                  Intelligent job matching powered by GPT-4o
                </p>
              </div>
            </div>
            {userEmail && (
              <div className="flex items-center gap-2 text-sm text-gray-700">
                <Mail className="w-4 h-4" />
                {userEmail}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Resume Upload & Controls */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="p-6" data-testid="resume-upload-card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                📄 Upload Resume
              </h2>
              <ResumeUpload onUploadSuccess={handleResumeUpload} />
            </Card>

            <Card className="p-6" data-testid="workflow-controls-card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                🎯 Workflow Control
              </h2>
              <Button
                onClick={handleExecuteWorkflow}
                disabled={!resumeId || isExecuting}
                className="w-full"
                size="lg"
                data-testid="execute-workflow-btn"
              >
                {isExecuting ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Executing...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5 mr-2" />
                    Run Job Matcher
                  </>
                )}
              </Button>

              {workflowStatus.status && (
                <div className="mt-4 p-4 rounded-lg bg-gray-50">
                  <p className="text-sm font-medium text-gray-700">
                    Status:
                    <span
                      className={`ml-2 px-2 py-1 rounded text-xs ${
                        workflowStatus.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : workflowStatus.status === 'failed'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}
                    >
                      {workflowStatus.status}
                    </span>
                  </p>
                  {workflowStatus.jobs_found !== undefined && (
                    <p className="text-sm text-gray-600 mt-2">
                      Jobs found: {workflowStatus.jobs_found}
                    </p>
                  )}
                  {workflowStatus.jobs_matched !== undefined && (
                    <p className="text-sm text-gray-600">
                      Matched: {workflowStatus.jobs_matched}
                    </p>
                  )}
                </div>
              )}
            </Card>

            <Card className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50">
              <h3 className="text-sm font-semibold text-gray-900 mb-2">
                ℹ️ How It Works
              </h3>
              <ul className="text-xs text-gray-700 space-y-1">
                <li>• Upload your resume (PDF or text)</li>
                <li>• AI extracts your skills & experience</li>
                <li>• Searches 8+ job boards (last 24 hours)</li>
                <li>• Matches jobs using GPT-4o</li>
                <li>• Sends results to your email</li>
              </ul>
            </Card>
          </div>

          {/* Right Panel - Workflow Visualization */}
          <div className="lg:col-span-2">
            <Card className="p-6 h-[calc(100vh-200px)]" data-testid="workflow-canvas-card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                🔄 Workflow Visualization
              </h2>
              <WorkflowCanvas status={workflowStatus.status} />
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;