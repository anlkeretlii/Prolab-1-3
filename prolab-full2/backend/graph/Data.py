from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Paper:
    """Makale bilgilerini tutan sınıf"""
    title: str
    doi: str
    authors: List[str]
    main_author: str

class Node:
    """Graf düğümü sınıfı"""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.papers: List[Paper] = []  # Yazarın makaleleri
        self.connections: Dict[int, int] = {}  # {connected_node_id: weight}
        
    def add_paper(self, paper: Paper):
        """Yazara makale ekle"""
        self.papers.append(paper)
    
    def add_connection(self, other_node_id: int):
        """Başka bir yazarla bağlantı ekle/güncelle"""
        self.connections[other_node_id] = self.connections.get(other_node_id, 0) + 1
    
    @property
    def paper_count(self) -> int:
        """Yazarın toplam makale sayısı"""
        return len(self.papers)
    
    @property
    def total_collaborations(self) -> int:
        """Yazarın toplam işbirliği sayısı"""
        return len(self.connections)

class CollaborationGraph:
    """Özel graf implementasyonu"""
    def __init__(self):
        self.nodes: Dict[int, Node] = {}  # {id: Node}
        self.name_to_id: Dict[str, int] = {}  # {name: id}
        self.next_id = 0
        
    def add_paper(self, paper: Paper):
        """Makaleyi grafa ekle ve yazarlar arası bağlantıları oluştur"""
        # Yazarları düğüm olarak ekle/güncelle
        author_ids = []
        for author_name in paper.authors:
            if author_name not in self.name_to_id:
                self.name_to_id[author_name] = self.next_id
                self.nodes[self.next_id] = Node(self.next_id, author_name)
                self.next_id += 1
            
            author_id = self.name_to_id[author_name]
            author_ids.append(author_id)
            self.nodes[author_id].add_paper(paper)
        
        # Ana yazar ve yardımcı yazarlar arasındaki bağlantıları oluştur
        main_author_name = paper.main_author
        if main_author_name not in self.name_to_id:
            self.name_to_id[main_author_name] = self.next_id
            self.nodes[self.next_id] = Node(self.next_id, main_author_name)
            self.next_id += 1
        
        main_author_id = self.name_to_id[main_author_name]
        for coauthor_id in author_ids:
            if coauthor_id != main_author_id:
                self.nodes[main_author_id].add_connection(coauthor_id)
                self.nodes[coauthor_id].add_connection(main_author_id)
    
    
    def get_average_paper_count(self) -> float:
        """Ortalama makale sayısını hesapla"""
        if not self.nodes:
            return 0
        total_papers = sum(node.paper_count for node in self.nodes.values())
        return total_papers / len(self.nodes)
    
    def get_node_size_and_color(self, node_id: int) -> tuple:
        """Düğümün boyut ve rengini hesapla"""
        avg_papers = self.get_average_paper_count()
        threshold = avg_papers * 0.2
        
        node_papers = self.nodes[node_id].paper_count
        
        if node_papers > avg_papers + threshold:
            return "large", "dark"
        elif node_papers < avg_papers - threshold:
            return "small", "light"
        else:
            return "medium", "normal"
    def dijkstra(self, start_id: int) -> tuple[dict, dict]:
        """Dijkstra algoritması ile tüm düğümler için en kısa yolları hesapla"""
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[start_id] = 0
        previous = {node_id: None for node_id in self.nodes}
        unvisited = set(self.nodes.keys())

        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])

            if distances[current] == float('inf'):
                break

            unvisited.remove(current)

            for neighbor, weight in self.nodes[current].connections.items():
                if neighbor in unvisited:
                    distance = distances[current] + (1.0 / weight)
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous[neighbor] = current

        return distances, previous
    def get_shortest_path(self, start_id: int, end_id: int) -> Optional[List[int]]:
        """İki yazar arasındaki en kısa yolu bul (Dijkstra algoritması)"""
        if start_id not in self.nodes or end_id not in self.nodes:
            return None
            
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[start_id] = 0
        previous = {node_id: None for node_id in self.nodes}
        unvisited = set(self.nodes.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])
            
            if current == end_id:
                break
                
            if distances[current] == float('inf'):
                break
                
            unvisited.remove(current)
            
            for neighbor, weight in self.nodes[current].connections.items():
                if neighbor in unvisited:
                    distance = distances[current] + (1.0 / weight)
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous[neighbor] = current
        
        if distances[end_id] == float('inf'):
            return None
            
        path = []
        current = end_id
        while current is not None:
            path.append(current)
            current = previous[current]
        
        return path[::-1]
    
    def get_shortest_path_with_queue(self, start_id: int, end_id: int) -> tuple[Optional[List[int]], List[int], dict]:
        """İki yazar arasındaki en kısa yolu ve son kuyruk adımını bul"""
        if start_id not in self.nodes or end_id not in self.nodes:
            return None, [], {}
            
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[start_id] = 0
        previous = {node_id: None for node_id in self.nodes}
        unvisited = set(self.nodes.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])
            
            if current == end_id:
                break
                
            if distances[current] == float('inf'):
                break
                
            unvisited.remove(current)
            
            for neighbor, weight in self.nodes[current].connections.items():
                if neighbor in unvisited:
                    distance = distances[current] + (1.0 / weight)
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous[neighbor] = current
        
        if distances[end_id] == float('inf'):
            return None, [], {}
            
        path = []
        current = end_id
        while current is not None:
            path.append(current)
            current = previous[current]
        
        final_queue = sorted(unvisited, key=lambda x: distances[x])
        return path[::-1], final_queue, distances

    def get_collaboration_count(self, author_id: int) -> int:
        """Bir yazarın işbirliği yaptığı yazar sayısını döndür"""
        if author_id not in self.nodes:
            return 0
        return self.nodes[author_id].total_collaborations
    
    def get_most_collaborative_author(self) -> Optional[tuple]:
        """En çok işbirliği yapan yazarı bul"""
        if not self.nodes:
            return None
            
        max_collabs = -1
        max_author_id = None
        
        for node_id, node in self.nodes.items():
            collab_count = node.total_collaborations
            if collab_count > max_collabs:
                max_collabs = collab_count
                max_author_id = node_id
        
        return (max_author_id, max_collabs) if max_author_id is not None else None
    def get_collaboration_count(self, author_id: int) -> int:
        """Bir yazarın işbirliği yaptığı yazar sayısını döndür"""
        if author_id not in self.nodes:
            return 0
        return len(self.nodes[author_id].connections)
    def find_longest_path(self, start_id: int) -> List[int]:
        """Bir yazardan başlayan en uzun yolu bul (DFS ile)"""
        if start_id not in self.nodes:
            return []
            
        visited = set()
        longest_path = []
        
        def dfs(current_id: int, current_path: List[int]):
            nonlocal longest_path
            visited.add(current_id)
            current_path.append(current_id)
            
            if len(current_path) > len(longest_path):
                longest_path = current_path.copy()
            
            # Komşuları ziyaret et
            for neighbor in self.nodes[current_id].connections:
                if neighbor not in visited:
                    dfs(neighbor, current_path)
            
            current_path.pop()
            visited.remove(current_id)
        
        dfs(start_id, [])
        return longest_path
    
    def find_longest_path(self, start_id: int) -> List[int]:
        """Bir yazardan başlayan en uzun yolu bul (DFS ile)"""
        if start_id not in self.nodes:
            return []
            
        visited = set()
        longest_path = []
        
        def dfs(current_id: int, current_path: List[int]):
            nonlocal longest_path
            visited.add(current_id)
            current_path.append(current_id)
            
            if len(current_path) > len(longest_path):
                longest_path = current_path.copy()
            
            # Komşuları ziyaret et
            for neighbor in self.nodes[current_id].connections:
                if neighbor not in visited:
                    dfs(neighbor, current_path)
            
            current_path.pop()
            visited.remove(current_id)
        
        dfs(start_id, [])
        return longest_path
class BSTNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1  # AVL tree için yükseklik bilgisi

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance_factor(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        if not node:
            return
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = max(self.height(y.left), self.height(y.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1

        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = max(self.height(x.left), self.height(x.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1

        return y

    def insert(self, key, data):
        if not self.root:
            self.root = BSTNode(key, data)
        else:
            self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if not node:
            return BSTNode(key, data)

        if key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)

        node.height = max(self.height(node.left), self.height(node.right)) + 1

        balance = self.balance_factor(node)

        # Sol Sol Durumu
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Sağ Sağ Durumu
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Sol Sağ Durumu
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Sağ Sol Durumu
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, key):
        if self.root:
            self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.data = temp.data
            node.right = self._delete(node.right, temp.key)

        if not node:
            return node

        node.height = max(self.height(node.left), self.height(node.right)) + 1

        balance = self.balance_factor(node)

        # Sol Sol Durumu
        if balance > 1 and self.balance_factor(node.left) >= 0:
            return self.right_rotate(node)

        # Sol Sağ Durumu
        if balance > 1 and self.balance_factor(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Sağ Sağ Durumu
        if balance < -1 and self.balance_factor(node.right) <= 0:
            return self.left_rotate(node)

        # Sağ Sol Durumu
        if balance < -1 and self.balance_factor(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node
    def _min_value_node(self, node):
        """Find the node with minimum key value in the given subtree"""
        current = node
        # Loop down to find the leftmost leaf
        while current.left:
            current = current.left
        return current
    def inorder(self):
        """Inorder traversal of the BST"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        """Helper method for inorder traversal"""
        if node:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)