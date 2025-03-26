import React, { useEffect, useState } from 'react';
import GraphVisualization from './components/GraphVisualization';
import ShortestPathForm from './components/ShortestPathForm';
import NodeInfo from './components/NodeInfo';
import MostCollaborativeAuthor from './components/MostCollaborativeAuthor';
import CollaborationCount from './components/CollaborationCount';
import LongestPath from './components/LongestPath';
import AuthorCollaborators from './components/AuthorCollaborators';
import SmallGraphVisualization from './components/SmallGraphVisualization';
import FindAuthor from './components/FindAuthor';
import AuthorShortestPaths from './components/AuthorShortestPaths';

import BSTVisualization from './components/BSTVisualization';
import { fetchGraphData, fetchShortestPath } from './main';
import './App.css';

const App = () => {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [highlightedPath, setHighlightedPath] = useState([]);
  const [output, setOutput] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [smallGraphData, setSmallGraphData] = useState({ nodes: [], edges: [] });
  const [authorId, setAuthorId] = useState('');
  const [startId, setStartId] = useState('');
  const [endId, setEndId] = useState('');

  useEffect(() => {
    const loadGraphData = async () => {
      try {
        const data = await fetchGraphData();
        setGraphData(data);
      } catch (err) {
        console.error('Error loading graph data:', err);
        setError('Error loading graph data');
      } finally {
        setLoading(false);
      }
    };

    loadGraphData();
  }, []);

  const handleShortestPathSearch = async () => {
    try {
      if (!startId || !endId) {
        setOutput(prev => [...prev, 'Start and end IDs are required']);
        return;
      }

      const response = await fetchShortestPath(startId, endId);
      
      if (!response || !response.path || !response.authors || !response.queue) {
        throw new Error('Invalid server response');
      }

      const { path, authors, queue } = response;
      setHighlightedPath(path);
      setOutput(prev => [...prev, `Shortest path: ${authors.join(' -> ')}`]);

      const finalNodes = queue.map(node => ({
        id: node.id,
        label: `${node.name}\n(${node.distance.toFixed(2)})`,
        color: '#e94560'
      }));

      setSmallGraphData({ nodes: finalNodes, edges: [] });

    } catch (err) {
      console.error('Error finding shortest path:', err);
      setOutput(prev => [...prev, `Error finding shortest path: ${err.message}`]);
    }
  };

  const handleNodeSelect = (node) => {
    setSelectedNode(node);
  };

  const handleCloseNodeInfo = () => {
    setSelectedNode(null);
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="container">
      <div className="output-area">
        <h3>Output</h3>
        <div className="output-content">
          {output.map((line, index) => (
            <div key={index} className="output-card">
              <p>{line}</p>
            </div>
          ))}
        </div>
        <div className="small-graph-area">
          <SmallGraphVisualization nodes={smallGraphData.nodes} edges={smallGraphData.edges} />
        </div>
      </div>
      <div className="graph-area">
        <GraphVisualization 
          nodes={graphData.nodes}
          edges={graphData.edges}
          highlightedPath={highlightedPath}
          onNodeSelect={handleNodeSelect}
        />
        {selectedNode && (
          <NodeInfo node={selectedNode} onClose={handleCloseNodeInfo} />
        )}
      </div>
      <div className="action-area">
        <input
          type="text"
          value={authorId}
          onChange={(e) => setAuthorId(e.target.value)}
          placeholder="Enter Author ID"
        />
        
          <FindAuthor authorId={authorId} setOutput={setOutput} setHighlightedPath={setHighlightedPath} />
          <AuthorCollaborators authorId={authorId} setOutput={setOutput} setSmallGraphData={setSmallGraphData} />
          <CollaborationCount authorId={authorId} setOutput={setOutput} />
          <AuthorShortestPaths authorId={authorId} setOutput={setOutput} setHighlightedPath={setHighlightedPath} />
          <MostCollaborativeAuthor setOutput={setOutput} />
          <LongestPath
            authorId={authorId}
            setOutput={setOutput}
            setHighlightedPath={setHighlightedPath}
          />
          <div className="shared-inputs">
          <input
            type="text"
            value={startId}
            onChange={(e) => setStartId(e.target.value)}
            placeholder="Start Author ID"
          />
          <input
            type="text"
            value={endId}
            onChange={(e) => setEndId(e.target.value)}
            placeholder="End Author ID"
          />
        </div>
        <div className="actions">
          <ShortestPathForm
            startId={startId}
            endId={endId}
            onSearch={handleShortestPathSearch}
          />
          <BSTVisualization
            startId={startId}
            endId={endId}
            setOutput={setOutput}
            setSmallGraphData={setSmallGraphData}
          />
        </div>
      </div>
    </div>
  );
};

export default App;

