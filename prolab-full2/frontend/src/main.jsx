import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
    <App />

)
export const fetchGraphData = async () => {
  const response = await fetch('http://localhost:5000/api/graph');  // Tam URL kullanın
  if (!response.ok) {
    throw new Error('Graf verisi yüklenemedi');
  }
  return response.json();
};
export const fetchMostCollaborativeAuthor = async () => {
  const response = await fetch('http://localhost:5000/api/most-collaborative');
  if (!response.ok) {
    throw new Error('En çok işbirliği yapan yazar bulunamadı');
  }
  return response.json();
};
export const fetchCollaborationCount = async (authorId) => {
  const response = await fetch(`http://localhost:5000/api/collaboration-count?author_id=${authorId}`);
  if (!response.ok) {
    throw new Error('Yazar bulunamadı');
  }
  return response.json();
};
export const fetchLongestPath = async (authorId) => {
  const response = await fetch(`http://localhost:5000/api/longestpath?author_id=${authorId}`);
  if (!response.ok) {
    throw new Error('Yol bulunamadı');
  }
  return response.json();
};
export const fetchAuthorCollaborators = async (authorId) => {
  const response = await fetch(`http://localhost:5000/api/author-collaborators?author_id=${authorId}`);
  if (!response.ok) {
    throw new Error('Yazar bulunamadı');
  }
  return response.json();
};
export const fetchAuthorShortestPaths = async (authorId) => {
  const response = await fetch(`http://localhost:5000/api/author-shortest-paths?author_id=${authorId}`);
  if (!response.ok) {
    throw new Error('En kısa yollar bulunamadı');
  }
  return response.json();
};
export const fetchAuthorById = async (authorId) => {
  const response = await fetch(`http://localhost:5000/api/author?author_id=${authorId}`);
  if (!response.ok) {
    throw new Error('Yazar bulunamadı');
  }
  return response.json();
};
export const fetchShortestPath = async (startId, endId) => {
  try {
    const response = await fetch(`http://localhost:5000/api/shortestpath?start=${startId}&end=${endId}`);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'En kısa yol bulunamadı');
    }
    
    // Validate response data
    if (!data || !Array.isArray(data.path) || !Array.isArray(data.authors) || !Array.isArray(data.queue)) {
      throw new Error('Geçersiz sunucu yanıtı');
    }
    
    return data;
  } catch (err) {
    console.error('Fetch error:', err);
    throw err;
  }
};
export const createBST = async (startId, endId) => {
  const response = await fetch('http://localhost:5000/api/bst', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ start_id: startId, end_id: endId }),
  });
  if (!response.ok) {
    throw new Error('BST oluşturulamadı');
  }
  return response.json();
};

export const deleteFromBST = async (startId, endId, removeId) => {
  const response = await fetch('http://localhost:5000/api/bst/delete', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ start_id: startId, end_id: endId, remove_id: removeId }),
  });
  if (!response.ok) {
    throw new Error('Yazar silinemedi');
  }
  return response.json();
};