import React, { useState } from 'react';
import { fetchAuthorShortestPaths } from '../main.jsx';

const AuthorShortestPaths = ({ authorId, setOutput, setHighlightedPath }) => {
  const [error, setError] = useState(null);

  const handleFetchShortestPaths = async () => {
    try {
      const data = await fetchAuthorShortestPaths(authorId);
      setError(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        `Yazar ID: ${authorId} için en kısa yollar hesaplandı`,
      ]);
      setHighlightedPath(data.path); // Tüm yolları tek bir path olarak vurgula
    } catch (err) {
      setError('En kısa yollar bulunamadı');
      setOutput((prevOutput) => [
        ...prevOutput,
        'En kısa yollar bulunamadı',
      ]);
    }
  };

  return (
    <div>
      <button onClick={handleFetchShortestPaths}>En Kısa Yolları Hesapla</button>
    </div>
  );
};

export default AuthorShortestPaths;