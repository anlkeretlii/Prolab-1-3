import React, { useState, useEffect } from 'react';
import { fetchAuthorCollaborators } from '../main.jsx';

const AuthorCollaborators = ({ authorId, setOutput, setSmallGraphData }) => {
  const [queue, setQueue] = useState([]);
  const [error, setError] = useState(null);

  const handleFetchCollaborators = async () => {
    try {
      const data = await fetchAuthorCollaborators(authorId);
      setQueue(data.queue);
      setError(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        `Yazar ID: ${data.author.id}, İşbirliği Yaptığı Yazarlar: ${data.queue.map(c => `${c.name} (${c.paperCount})`).join(', ')}`,
      ]);

      // Küçük graf için verileri ayarla
      const smallNodes = [
        {
          id: data.author.id,
          label: data.author.name,
          size: Math.min(20, 5 + data.author.paperCount * 2),
          color: '#00ff00',
          papers: data.author.paperCount,
        },
        ...data.queue.map(collab => ({
          id: collab.id,
          label: collab.name,
          size: Math.min(20, 5 + collab.paperCount * 2),
          color: '#00ff00',
          papers: collab.paperCount,
        }))
      ];
      const smallEdges = data.queue.map(collab => ({
        from: data.author.id,
        to: collab.id,
        color: '#00ff00',
        width: 2,
      }));
      setSmallGraphData({ nodes: smallNodes, edges: smallEdges });
    } catch (err) {
      setError('Yazar bulunamadı');
      setQueue([]);
      setOutput((prevOutput) => [
        ...prevOutput,
        'Yazar bulunamadı',
      ]);
    }
  };

  useEffect(() => {
    if (queue.length > 0) {
      const interval = setInterval(() => {
        setQueue((prevQueue) => {
          const newQueue = [...prevQueue];
          newQueue.shift(); // Kuyruktan bir eleman çıkar
          return newQueue;
        });
      }, 1000); // Her saniyede bir eleman çıkar

      return () => clearInterval(interval);
    }
  }, [queue]);

  return (
    <div>
      <button onClick={handleFetchCollaborators}>İşbirliği Yapan Yazarları Bul</button>
      
    </div>
  );
};

export default AuthorCollaborators;