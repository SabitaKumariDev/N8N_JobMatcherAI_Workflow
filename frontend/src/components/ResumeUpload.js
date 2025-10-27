import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { toast } from 'sonner';
import { Upload, FileText, Loader2 } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ResumeUpload = ({ onUploadSuccess }) => {
  const [email, setEmail] = useState('');
  const [resumeText, setResumeText] = useState('');
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [activeTab, setActiveTab] = useState('text');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type === 'application/pdf' || selectedFile.name.endsWith('.pdf')) {
        setFile(selectedFile);
      } else {
        toast.error('Please upload a PDF file');
      }
    }
  };

  const handleUpload = async () => {
    if (!email) {
      toast.error('Please enter your email address');
      return;
    }

    if (activeTab === 'text' && !resumeText.trim()) {
      toast.error('Please paste your resume text');
      return;
    }

    if (activeTab === 'file' && !file) {
      toast.error('Please select a PDF file');
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('user_email', email);

      if (activeTab === 'text') {
        formData.append('resume_text', resumeText);
      } else {
        formData.append('file', file);
      }

      const response = await axios.post(`${API}/resume/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      const resumeData = response.data;
      toast.success('Resume uploaded successfully!');
      onUploadSuccess(resumeData.id, email);

      // Reset form
      setResumeText('');
      setFile(null);
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Failed to upload resume');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-4" data-testid="resume-upload">
      <div>
        <Label htmlFor="email">Email Address</Label>
        <Input
          id="email"
          type="email"
          placeholder="your.email@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1"
          data-testid="email-input"
        />
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="text" data-testid="text-tab">
            <FileText className="w-4 h-4 mr-2" />
            Text
          </TabsTrigger>
          <TabsTrigger value="file" data-testid="file-tab">
            <Upload className="w-4 h-4 mr-2" />
            PDF
          </TabsTrigger>
        </TabsList>

        <TabsContent value="text" className="space-y-4">
          <div>
            <Label htmlFor="resume-text">Paste Your Resume</Label>
            <Textarea
              id="resume-text"
              placeholder="Paste your resume text here..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              rows={10}
              className="mt-1"
              data-testid="resume-text-input"
            />
          </div>
        </TabsContent>

        <TabsContent value="file" className="space-y-4">
          <div>
            <Label htmlFor="resume-file">Upload PDF Resume</Label>
            <div
              className="mt-1 border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors cursor-pointer"
              onClick={() => document.getElementById('resume-file').click()}
            >
              <input
                id="resume-file"
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="hidden"
                data-testid="resume-file-input"
              />
              {file ? (
                <div className="text-sm">
                  <FileText className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                  <p className="font-medium text-gray-900">{file.name}</p>
                  <p className="text-gray-500 mt-1">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              ) : (
                <div className="text-sm">
                  <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-gray-600">Click to upload PDF</p>
                  <p className="text-gray-400 text-xs mt-1">Maximum 5MB</p>
                </div>
              )}
            </div>
          </div>
        </TabsContent>
      </Tabs>

      <Button
        onClick={handleUpload}
        disabled={isUploading}
        className="w-full"
        data-testid="upload-resume-btn"
      >
        {isUploading ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Uploading...
          </>
        ) : (
          <>
            <Upload className="w-4 h-4 mr-2" />
            Upload Resume
          </>
        )}
      </Button>
    </div>
  );
};

export default ResumeUpload;