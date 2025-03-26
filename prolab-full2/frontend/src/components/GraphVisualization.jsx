import React, { useEffect, useRef } from 'react';
import { Network } from 'vis-network';

const GraphVisualization = ({ nodes, edges, highlightedPath, onNodeSelect }) => {
  const networkRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    const options = {
      nodes: {
        shape: 'dot',
        font: {
          size: 12,
          color: '#dcdedd',
          face: 'Roboto'
        },
        borderWidth: 2,
        shadow: false,
      },
      edges: {
        width: 1,
        color: { color: '#533483', highlight: '#e94560' },
        smooth: {
          type: 'continuous',
          forceDirection: 'none'
        }
      },
      physics: {
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -26,
          springLength: 100,
          springConstant: 0.01,
          damping: 0.4,
        },
        stabilization: {
          iterations: 400
        },
        adaptiveTimestep: true,
        
      },
      layout:{
        improvedLayout: false
      },
      interaction: {
        hideEdgesOnDrag: true,
        hideEdgesOnZoom: true,
        multiselect: false,
        dragNodes: true,
      },
    };

    const container = containerRef.current;
    const data = {
      nodes: nodes.map(node => ({
        ...node,
        size: Math.min(30, 10 + node.collaborationCount * 2),
        papers: node.papers || [], // Makale bilgilerini ekle
      })),
      edges,
    };

    const network = new Network(container, data, options);
    networkRef.current = network;

    network.on('click', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = nodes.find((n) => n.id === nodeId);
        onNodeSelect(node);
      } else {
        onNodeSelect(null);
      }
    });

    network.on('stabilizationIterationsDone', () => {
      network.setOptions({ physics: { enabled: true }});
    });

    return () => {
      network.destroy();
    };
  }, [nodes, edges]);

  useEffect(() => {
    if (highlightedPath.length > 0) {
      const updatedNodes = nodes.map((node) => {
        if (highlightedPath.includes(node.id)) {
          return { ...node, color: { background: '#e94560', border: '#16213e' } };
        }
        return node;
      });

      const updatedEdges = edges.map((edge) => {
        if (highlightedPath.includes(edge.from) && highlightedPath.includes(edge.to)) {
          return { ...edge, color: '#e94560', width: 3 };
        }
        return { ...edge, color: '#533483', width: 1 };
      });
      networkRef.current.setData({ nodes: updatedNodes, edges: updatedEdges });
      networkRef.current.stabilize();
    }
  }, [highlightedPath]);
  return (
    <div ref={containerRef} style={{ height: '100%', width: '100%' }}></div>
  );
};

export default GraphVisualization;