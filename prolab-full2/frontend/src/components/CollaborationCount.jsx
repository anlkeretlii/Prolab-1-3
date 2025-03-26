import React, { useState } from 'react';
import { fetchCollaborationCount } from '../main.jsx';

const CollaborationCount = ({ authorId, setOutput }) => {
  const [collaborationCount, setCollaborationCount] = useState(null);
  const [error, setError] = useState(null);

  const handleFetchCollaborationCount = async () => {
    try {
      const data = await fetchCollaborationCount(authorId);
      setCollaborationCount(data.collaborationCount);
      setError(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        `Yazar ID: ${data.author_id}, İşbirliği Sayısı: ${data.collaborationCount}`,
      ]);
    } catch (err) {
      setError('Yazar bulunamadı');
      setCollaborationCount(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        'Yazar bulunamadı',
      ]);
    }
  };

  return (
    <div>
      <button onClick={handleFetchCollaborationCount}>İşbirliği Sayısını Bul</button>
    </div>
  );
};

export default CollaborationCount;