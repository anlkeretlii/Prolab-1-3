import React, { useState } from 'react';
import { createBST, deleteFromBST } from '../main.jsx';

const BSTVisualization = ({ startId, endId, setOutput, setSmallGraphData }) => {
  const [removeId, setRemoveId] = useState('');
  const [bst, setBST] = useState([]);
  const [error, setError] = useState(null);

  const handleCreateBST = async () => {
    try {
      if (!startId || !endId) {
        setError('Yazar ID eksik');
        return;
      }
      const data = await createBST(startId, endId);
      setBST(data.bst);
      setError(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        `En kısa yol üzerindeki yazarlardan BST oluşturuldu`,
      ]);

      setSmallGraphData({
        nodes: data.nodes,
        edges: data.edges
      });
    } catch (err) {
      setError('BST oluşturulamadı');
      setBST([]);
      setOutput((prevOutput) => [
        ...prevOutput,
        'BST oluşturulamadı',
      ]);
    }
  };

  const handleDeleteFromBST = async () => {
    try {
      if (!startId || !endId || !removeId) {
        setError('Yazar ID eksik');
        return;
      }
      const data = await deleteFromBST(startId, endId, removeId);
      setBST(data.bst);
      setError(null);
      setOutput((prevOutput) => [
        ...prevOutput,
        `BST'den yazar ID: ${removeId} silindi`,
      ]);

      setSmallGraphData({
        nodes: data.nodes,
        edges: data.edges
      });
    } catch (err) {
      setError('Yazar silinemedi');
      setOutput((prevOutput) => [
        ...prevOutput,
        'Yazar silinemedi',
      ]);
    }
  };

  return (
    <div>
      <button onClick={handleCreateBST}>BST Oluştur</button>
      <div>
        <input
          type="text"
          value={removeId}
          onChange={(e) => setRemoveId(e.target.value)}
          placeholder="Silinecek Yazar ID"
        />
        <button onClick={handleDeleteFromBST}>Yazarı BST'den Sil</button>
      </div>
      
    </div>
  );
};

export default BSTVisualization;