import React, { useState } from 'react';
import { fetchLongestPath } from '../main.jsx';

const LongestPath = ({ authorId, setOutput, setHighlightedPath }) => {
  const [path, setPath] = useState(null);
  const [error, setError] = useState(null);

  const handleFetchLongestPath = async () => {
    try {
      const data = await fetchLongestPath(authorId);
      setPath(data.path);
      setError(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        `Yazar ID: ${authorId}, En uzun yol: ${data.authors.join(' -> ')}, Uzunluk: ${data.length}`,
      ]);
      setHighlightedPath(data.path); // Set the highlighted path
    } catch (err) {
      setError('Yol bulunamadı');
      setPath(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        'Yol bulunamadı',
      ]);
    }
  };

  return (
    <div>
      <button onClick={handleFetchLongestPath}>En Uzun Yolu Bul</button>
    </div>
  );
};

export default LongestPath;