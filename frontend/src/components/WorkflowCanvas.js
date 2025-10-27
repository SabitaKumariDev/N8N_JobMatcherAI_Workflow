import React, { useCallback, useMemo } from 'react';
import ReactFlow, {
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType
} from 'reactflow';
import 'reactflow/dist/style.css';
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
    </div>
  );
};

const nodeTypes = {
  workflow: WorkflowNode
};

const WorkflowCanvas = ({ status }) => {
  const initialNodes = useMemo(
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
        position: { x: 250, y: 120 },
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
        position: { x: 50, y: 260 },
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
        position: { x: 450, y: 260 },
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
        position: { x: 250, y: 400 },
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

  const initialEdges = [
    {
      id: 'e1-2',
      source: '1',
      target: '2',
      animated: status === 'running',
      markerEnd: { type: MarkerType.ArrowClosed }
    },
    {
      id: 'e2-3',
      source: '2',
      target: '3',
      animated: status === 'running',
      markerEnd: { type: MarkerType.ArrowClosed }
    },
    {
      id: 'e2-4',
      source: '2',
      target: '4',
      animated: status === 'running',
      markerEnd: { type: MarkerType.ArrowClosed }
    },
    {
      id: 'e3-5',
      source: '3',
      target: '5',
      animated: status === 'running',
      markerEnd: { type: MarkerType.ArrowClosed }
    },
    {
      id: 'e4-5',
      source: '4',
      target: '5',
      animated: status === 'running',
      markerEnd: { type: MarkerType.ArrowClosed }
    }
  ];

  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div className="h-full w-full" data-testid="workflow-canvas">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
      >
        <Background color="#e5e7eb" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  );
};

export default WorkflowCanvas;