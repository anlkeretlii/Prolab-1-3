import React from 'react';

const ShortestPathForm = ({ startId, endId, onSearch }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!startId || !endId) {
      alert('Başlangıç ve bitiş ID\'leri gerekli');
      return;
    }
    onSearch();
  };

  return (
    <div>
      <button 
        onClick={handleSubmit}
        disabled={!startId || !endId}
      >
        En Kısa Yolu Bul
      </button>
    </div>
  );
};

export default ShortestPathForm;