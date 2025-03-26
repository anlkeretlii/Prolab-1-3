import React, { useState } from 'react';

const NodeInfo = ({ node, onClose }) => {
  const [showPopup, setShowPopup] = useState(false);

  const handleReadMore = () => {
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    setShowPopup(false);
  };

  if (!node) return null;

  return (
    <>
      <div className="node-info">
        <p>ID: {node.id}</p>
        <p>İsim: {node.label}</p>
        <p>Makale Sayısı: {node.paperCount}</p>
        <p>İşbirliği Sayısı: {node.collaborationCount}</p>
        <button onClick={handleReadMore}>Devamını Oku</button>
        <button onClick={onClose}>Kapat</button>
      </div>
      {showPopup && (
        <>
          <div className="popup-overlay" onClick={handleClosePopup}></div>
          <div className="popup">
            <h3>Yazar Bilgileri</h3>
            <p>ID: {node.id}</p>
            <p>İsim: {node.label}</p>
            <p>Makale Sayısı: {node.paperCount}</p>
            <p>İşbirliği Sayısı: {node.collaborationCount}</p>
            <h4>Makaleler</h4>
            <div className="scrollable-panel">
              <ul>
                {node.papers && node.papers.length > 0 ? (
                  node.papers.map((paper, index) => (
                    <li key={index}>{paper.title}</li>
                  ))
                ) : (
                  <li>Makale bulunamadı</li>
                )}
              </ul>
            </div>
            <button onClick={handleClosePopup}>Kapat</button>
          </div>
        </>
      )}
    </>
  );
};

export default NodeInfo;