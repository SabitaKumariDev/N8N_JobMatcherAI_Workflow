import React from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ExternalLink, MapPin, Building2, Calendar } from 'lucide-react';

const JobMatchCard = ({ job, index }) => {
  const matchScoreColor = (score) => {
    if (score >= 80) return 'bg-green-100 text-green-800 border-green-200';
    if (score >= 70) return 'bg-blue-100 text-blue-800 border-blue-200';
    if (score >= 60) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-gray-100 text-gray-800 border-gray-200';
  };

  return (
    <Card
      className="p-6 hover:shadow-lg transition-shadow"
      data-testid={`job-match-card-${index}`}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h3 className="text-xl font-semibold text-gray-900">
              {index}. {job.title}
            </h3>
            <Badge
              className={`${matchScoreColor(job.match_score || 0)}`}
              data-testid="match-score-badge"
            >
              {Math.round(job.match_score || 0)}% Match
            </Badge>
          </div>

          <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
            <div className="flex items-center gap-1">
              <Building2 className="w-4 h-4" />
              {job.company}
            </div>
            {job.location && (
              <div className="flex items-center gap-1">
                <MapPin className="w-4 h-4" />
                {job.location}
              </div>
            )}
            <div className="flex items-center gap-1">
              <Calendar className="w-4 h-4" />
              {job.source.charAt(0).toUpperCase() + job.source.slice(1)}
            </div>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <p className="text-sm text-gray-700 mb-2">
          <strong>Why it matches:</strong>
        </p>
        <p className="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg">
          {job.match_reason || 'Good fit based on your skills and experience'}
        </p>
      </div>

      {job.description && (
        <p className="text-sm text-gray-600 mb-4 line-clamp-2">
          {job.description}
        </p>
      )}

      <div className="flex items-center gap-3">
        <Button
          asChild
          className="flex-1"
          data-testid="view-job-btn"
        >
          <a
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-2"
          >
            View Job
            <ExternalLink className="w-4 h-4" />
          </a>
        </Button>
      </div>
    </Card>
  );
};

export default JobMatchCard;