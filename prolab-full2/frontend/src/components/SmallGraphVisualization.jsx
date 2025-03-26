import React, { useEffect, useRef } from 'react';
import { Network } from 'vis-network';

const SmallGraphVisualization = ({ nodes, edges }) => {
  const networkRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    const options = {
      nodes: {
        shape: 'circle',
        size: 30,
        font: {
          size: 14,
          color: '#000000',
        },
        borderWidth: 2,
        shadow: false
      },
      edges: {
        width: 2,
        smooth: {
          type: 'continuous'
        }
      },
      layout: {
        hierarchical: {
          enabled: true,
          direction: 'LR',
          sortMethod: 'directed',
          nodeSpacing: 150,
          levelSeparation: 150
        }
      },
      physics: false,
      interaction: {
        dragNodes: false,
        dragView: true,
        zoomView: true
      }
    };

    const container = containerRef.current;
    const data = {
      nodes: nodes,
      edges: edges
    };

    const network = new Network(container, data, options);
    networkRef.current = network;

    network.fit();

    return () => {
      network.destroy();
    };
  }, [nodes, edges]);

  return (
    <div ref={containerRef} style={{ height: '300px', width: '100%' }}></div>
  );
};

export default SmallGraphVisualization;