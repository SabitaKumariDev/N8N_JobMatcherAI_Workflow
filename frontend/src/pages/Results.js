import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import JobMatchCard from '../components/JobMatchCard';
import { ArrowLeft, RefreshCw, Mail } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [matchedJobs, setMatchedJobs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const userEmail = location.state?.userEmail;

  useEffect(() => {
    // Load from state or fetch from API
    if (location.state?.matchedJobs) {
      setMatchedJobs(location.state.matchedJobs);
      setIsLoading(false);
    } else if (userEmail) {
      fetchJobMatches();
    } else {
      setIsLoading(false);
    }
  }, []);

  const fetchJobMatches = async () => {
    try {
      const response = await axios.get(
        `${API}/jobs/matches/${encodeURIComponent(userEmail)}`
      );
      setMatchedJobs(response.data);
    } catch (error) {
      console.error('Error fetching job matches:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-700">Loading your job matches...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                onClick={() => navigate('/')}
                data-testid="back-to-dashboard-btn"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Dashboard
              </Button>
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

      {/* Results */}
      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🎯 Your Job Matches
          </h1>
          <p className="text-gray-600">
            Found {matchedJobs.length} jobs matching your profile
          </p>
        </div>

        {matchedJobs.length === 0 ? (
          <Card className="p-12 text-center">
            <div className="max-w-md mx-auto">
              <div className="text-6xl mb-4">🔍</div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                No matches found
              </h2>
              <p className="text-gray-600 mb-6">
                We couldn't find any jobs matching your profile in the last 24
                hours. Try again later or update your resume.
              </p>
              <Button onClick={() => navigate('/')}>Back to Dashboard</Button>
            </div>
          </Card>
        ) : (
          <div className="space-y-4" data-testid="job-matches-list">
            {matchedJobs.map((job, index) => (
              <JobMatchCard key={index} job={job} index={index + 1} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Results;