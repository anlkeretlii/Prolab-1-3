import React, { useState } from 'react';
import { fetchAuthorById } from '../main.jsx';

const FindAuthor = ({ authorId, setOutput, setHighlightedPath }) => {
  const [author, setAuthor] = useState(null);
  const [error, setError] = useState(null);

  const handleFetchAuthor = async () => {
    try {
      const data = await fetchAuthorById(authorId);
      setAuthor(data);
      setError(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        `Yazar ID: ${data.id}, İsim: ${data.name}, Makale Sayısı: ${data.paperCount}, İşbirliği Sayısı: ${data.collaborationCount}`,
      ]);
      setHighlightedPath([data.id]); // Yazarı grafikte vurgula
    } catch (err) {
      setError('Yazar bulunamadı');
      setAuthor(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        'Yazar bulunamadı',
      ]);
    }
  };

  return (
    <div>
      <button onClick={handleFetchAuthor}>Yazarı Bul</button>
    </div>
  );
};

export default FindAuthor;