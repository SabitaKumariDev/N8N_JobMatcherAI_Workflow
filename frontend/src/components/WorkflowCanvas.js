import React from 'react';
import { ReactFlow, Controls, Background, MarkerType, Handle, Position } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import {
  FileText,
  Brain,
  Search,
  Target,
  Mail,
  CheckCircle2
} from 'lucide-react';

const WorkflowNode = ({ data }) => {
  const statusColors = {
    pending: 'bg-gray-100 text-gray-700',
    running: 'bg-blue-100 text-blue-700',
    completed: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700'
  };

  const Icon = data.icon;

  return (
    <div className="workflow-node" data-testid={`workflow-node-${data.label}`}>
      <Handle type="target" position={Position.Top} />
      <div className="workflow-node-header">
        <div className="workflow-node-icon">
          <Icon size={16} />
        </div>
        <div className="workflow-node-title">{data.label}</div>
      </div>
      <div className="workflow-node-desc">{data.description}</div>
      {data.status && (
        <div
          className={`workflow-node-status ${data.status} ${statusColors[data.status]}`}
        >
          {data.status === 'completed' && <CheckCircle2 className="w-3 h-3 inline mr-1" />}
          {data.status.toUpperCase()}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

const nodeTypes = {
  workflow: WorkflowNode
};

const WorkflowCanvas = ({ status }) => {
  const nodes = useMemo(
    () => [
      {
        id: '1',
        type: 'workflow',
        position: { x: 250, y: 0 },
        data: {
          label: 'Upload Resume',
          description: 'Upload your resume (PDF or text)',
          icon: FileText,
          status: status === 'running' || status === 'completed' ? 'completed' : 'pending'
        }
      },
      {
        id: '2',
        type: 'workflow',
        position: { x: 250, y: 140 },
        data: {
          label: 'Parse Resume',
          description: 'Extract skills using GPT-4o',
          icon: Brain,
          status:
            status === 'running'
              ? 'running'
              : status === 'completed'
              ? 'completed'
              : 'pending'
        }
      },
      {
        id: '3',
        type: 'workflow',
        position: { x: 50, y: 280 },
        data: {
          label: 'Fetch Jobs',
          description: 'Search 8+ job boards (24h)',
          icon: Search,
          status:
            status === 'running'
              ? 'running'
              : status === 'completed'
              ? 'completed'
              : 'pending'
        }
      },
      {
        id: '4',
        type: 'workflow',
        position: { x: 450, y: 280 },
        data: {
          label: 'Match Jobs',
          description: 'AI-powered job matching',
          icon: Target,
          status:
            status === 'running'
              ? 'running'
              : status === 'completed'
              ? 'completed'
              : 'pending'
        }
      },
      {
        id: '5',
        type: 'workflow',
        position: { x: 250, y: 420 },
        data: {
          label: 'Send Email',
          description: 'Email matched jobs to you',
          icon: Mail,
          status: status === 'completed' ? 'completed' : 'pending'
        }
      }
    ],
    [status]
  );

  const edges = useMemo(
    () => [
      {
        id: 'e1-2',
        source: '1',
        target: '2',
        type: 'smoothstep',
        animated: status === 'running',
        style: { stroke: '#3b82f6', strokeWidth: 2 },
        markerEnd: { 
          type: MarkerType.ArrowClosed,
          color: '#3b82f6',
          width: 20,
          height: 20
        }
      },
      {
        id: 'e2-3',
        source: '2',
        target: '3',
        type: 'smoothstep',
        animated: status === 'running',
        style: { stroke: '#3b82f6', strokeWidth: 2 },
        markerEnd: { 
          type: MarkerType.ArrowClosed,
          color: '#3b82f6',
          width: 20,
          height: 20
        }
      },
      {
        id: 'e2-4',
        source: '2',
        target: '4',
        type: 'smoothstep',
        animated: status === 'running',
        style: { stroke: '#3b82f6', strokeWidth: 2 },
        markerEnd: { 
          type: MarkerType.ArrowClosed,
          color: '#3b82f6',
          width: 20,
          height: 20
        }
      },
      {
        id: 'e3-5',
        source: '3',
        target: '5',
        type: 'smoothstep',
        animated: status === 'running',
        style: { stroke: '#3b82f6', strokeWidth: 2 },
        markerEnd: { 
          type: MarkerType.ArrowClosed,
          color: '#3b82f6',
          width: 20,
          height: 20
        }
      },
      {
        id: 'e4-5',
        source: '4',
        target: '5',
        type: 'smoothstep',
        animated: status === 'running',
        style: { stroke: '#3b82f6', strokeWidth: 2 },
        markerEnd: { 
          type: MarkerType.ArrowClosed,
          color: '#3b82f6',
          width: 20,
          height: 20
        }
      }
    ],
    [status]
  );

  return (
    <div className="h-full w-full" data-testid="workflow-canvas">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
        minZoom={0.5}
        maxZoom={1.5}
        defaultEdgeOptions={{
          type: 'smoothstep',
          animated: false
        }}
      >
        <Background color="#e5e7eb" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  );
};

export default WorkflowCanvas;