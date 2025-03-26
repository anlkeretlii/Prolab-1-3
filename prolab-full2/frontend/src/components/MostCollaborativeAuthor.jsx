import React, { useState } from 'react';
import { fetchMostCollaborativeAuthor } from '../main.jsx';

const MostCollaborativeAuthor = ({ setOutput }) => {
  const [author, setAuthor] = useState(null);
  const [error, setError] = useState(null);

  const handleFetchAuthor = async () => {
    try {
      const data = await fetchMostCollaborativeAuthor();
      setAuthor(data);
      setError(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        `En çok işbirliği yapan yazar: ${data.name} (ID: ${data.id}, İşbirliği Sayısı: ${data.collaborationCount})`,
      ]);
    } catch (err) {
      setError('En çok işbirliği yapan yazar bulunamadı');
      setAuthor(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        'En çok işbirliği yapan yazar bulunamadı',
      ]);
    }
  };

  return (
    <div>
      <button onClick={handleFetchAuthor}>En Çok İşbirliği Yapan Yazarı Bul</button>
      
    </div>
  );
};

export default MostCollaborativeAuthor;