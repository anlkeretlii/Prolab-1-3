from flask import Flask, jsonify, request
from flask_cors import CORS
from graph.Data import CollaborationGraph, Paper, BinarySearchTree,BSTNode
from graph.Preprocessor import DataPreprocessor
import json
from collections import deque
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Herkese izin ver
# CollaborationGraph sınıfınızdan bir instance oluştur
graph = CollaborationGraph()  # Sizin mevcut graph sınıfınız
preprocessor = DataPreprocessor()
df = preprocessor.load_and_clean_data('../data/veriseti.xlsx')
for _, row in df.iterrows():
    paper = Paper(
        title=row['paper_title'],
        doi=row['doi'],
        authors=row['coauthors'],
        main_author=row['author_name']
    )
    
    graph.add_paper(paper)
@app.route('/api/collaboration-count', methods=['GET'])
def get_collaboration_count():
    """Belirli bir yazarın işbirliği yaptığı yazar sayısını döndür"""
    author_id = int(request.args.get('author_id'))
    collaboration_count = graph.get_collaboration_count(author_id)
    if collaboration_count is None:
        return jsonify({'error': 'Yazar bulunamadı'}), 404
    return jsonify({
        'author_id': author_id,
        'collaborationCount': collaboration_count
    })
@app.route('/api/longestpath', methods=['GET'])
def get_longest_path():
    """Belirli bir yazarın gidebileceği en uzun yolu döndür"""
    author_id = int(request.args.get('author_id'))
    path = graph.find_longest_path(author_id)
    if not path:
        return jsonify({'error': 'Yol bulunamadı'}), 404
    return jsonify({
        'path': path,
        'length': len(path),
        'authors': [graph.nodes[node_id].name for node_id in path]
    })

@app.route('/api/author-collaborators', methods=['GET'])
def get_author_collaborators():
    """Belirli bir yazar ve işbirliği yaptığı yazarlar için düğüm ağırlıklarına göre kuyruk oluştur"""
    author_id = int(request.args.get('author_id'))
    if author_id not in graph.nodes:
        return jsonify({'error': 'Yazar bulunamadı'}), 404

    author = graph.nodes[author_id]
    collaborators = [(collab_id, graph.nodes[collab_id].paper_count) for collab_id in author.connections]
    collaborators.sort(key=lambda x: x[1], reverse=True)  # Düğüm ağırlıklarına göre sırala

    # Kuyruk oluştur
    queue = deque(collaborators)

    return jsonify({
        'author': {
            'id': author.id,
            'name': author.name,
            'paperCount': author.paper_count
        },
        'queue': [
            {'id': collab_id, 'name': graph.nodes[collab_id].name, 'paperCount': paper_count}
            for collab_id, paper_count in queue
        ]
    })


@app.route('/api/author-shortest-paths', methods=['GET'])
def get_author_shortest_paths():
    """Belirli bir yazar ve işbirlikçi yazarlar arasında en kısa yolları hesapla"""
    author_id = int(request.args.get('author_id'))
    if author_id not in graph.nodes:
        return jsonify({'error': 'Yazar bulunamadı'}), 404

    # Dijkstra algoritmasını bir kez çalıştırarak tüm düğümler için en kısa yolları hesapla
    distances, previous = graph.dijkstra(author_id)

    # İşbirlikçi yazarlar ve onların işbirlikçileri arasında en kısa yolları hesapla
    shortest_paths = []
    for node_id in graph.nodes:
        if node_id != author_id and distances[node_id] != float('inf'):
            path = []
            current = node_id
            while current is not None:
                path.append(current)
                current = previous[current]
            shortest_paths.extend(path[::-1])

    # Tekrarlanan node_id'leri kaldır
    shortest_paths = list(dict.fromkeys(shortest_paths))

    return jsonify({'path': shortest_paths})

@app.route('/api/graph', methods=['GET'])
def get_graph_data():
    """Tüm graf verisini döndür"""
    nodes = []
    edges = []
    
    # Graf verilerini VisJS formatına dönüştür
    for node_id, node in graph.nodes.items():
        # Ortalama makale sayısını hesapla
        avg_papers = graph.get_average_paper_count()
        threshold = avg_papers * 0.2
        
        # Düğüm boyutu ve rengini belirle
        size, color = graph.get_node_size_and_color(node_id)
        
        # Node boyutlarını ayarla
        node_size = {
            "small": 10,
            "medium": 20,
            "large": 30,
        }.get(size, 10)
        node_color = {
            "light": "#c940e5",  # Accent color
            "normal": "#a030b8",  # Slightly darker
            "dark": "#7b208b",    # Even darker
        }.get(color, "#c940e5")
        nodes.append({
            'id': node_id,
            'label': node.name,
            'size': node_size,
            'color': node_color,
            'paperCount': len(node.papers),
            'collaborationCount': len(node.connections),
            'papers': [{'title': paper.title} for paper in node.papers]  # Makale bilgilerini ekle
        })
        
        # Kenarları ekle
        for connected_id, weight in node.connections.items():
            if node_id < connected_id:  # Her kenarı sadece bir kez ekle
                edges.append({
                    'from': node_id,
                    'to': connected_id,
                    'weight': weight,
                    'title': f'İşbirliği Sayısı: {weight}',  # Edge üzerinde hover olunca görünecek
                    'color': {
                        'color': '#4a4a5e',  # Edge color
                        'highlight': '#c940e5'  # Highlight color when selected
                    }
                })
    
    return jsonify({
        'nodes': nodes,
        'edges': edges
    })
    
@app.route('/api/author', methods=['GET'])
def get_author_by_id():
    """Belirli bir yazarın bilgilerini döndür"""
    author_id = int(request.args.get('author_id'))
    if author_id not in graph.nodes:
        return jsonify({'error': 'Yazar bulunamadı'}), 404

    author = graph.nodes[author_id]
    return jsonify({
        'id': author.id,
        'name': author.name,
        'paperCount': author.paper_count,
        'collaborationCount': author.total_collaborations
    })
@app.route('/api/bst', methods=['POST'])
def create_bst():
    """En kısa yoldaki yazarlardan BST oluştur"""
    data = request.json
    start_id = int(data['start_id'])
    end_id = int(data['end_id'])
    
    # En kısa yolu bul
    path = graph.get_shortest_path(start_id, end_id)
    if not path:
        return jsonify({'error': 'Yol bulunamadı'}), 404

    # Yoldaki yazarlardan BST oluştur
    bst = BinarySearchTree()
    for node_id in path:
        author_data = {
            'id': node_id,
            'name': graph.nodes[node_id].name,
            'paperCount': graph.nodes[node_id].paper_count
        }
        bst.insert(graph.nodes[node_id].paper_count, author_data)

    # BST'yi graph formatına dönüştür
    nodes = []
    edges = []
    
    def traverse_bst(node, x=0, y=0):
        if node:
            current_id = node.data['id']
            nodes.append({
                'id': current_id,
                'label': f"{node.data['name']}\n({node.data['paperCount']})",
                'x': x,
                'y': y,
                'fixed': {
                    'x': True,
                    'y': True
                }
            })
            
            if node.left:
                left_id = node.left.data['id']
                edges.append({
                    'from': current_id,
                    'to': left_id
                })
                # Sol çocuk için x koordinatını azalt, y koordinatını artır
                traverse_bst(node.left, x - 200, y + 100)
                
            if node.right:
                right_id = node.right.data['id']
                edges.append({
                    'from': current_id,
                    'to': right_id
                })
                # Sağ çocuk için x koordinatını artır, y koordinatını artır
                traverse_bst(node.right, x + 200, y + 100)
    
    # Kök düğümden başlayarak ağacı dolaş
    if bst.root:
        traverse_bst(bst.root)
    
    return jsonify({
        'bst': bst.inorder(),
        'nodes': nodes,
        'edges': edges
    })

@app.route('/api/bst/delete', methods=['POST'])
def delete_from_bst():
    """BST'den bir yazarı sil"""
    data = request.json
    start_id = int(data['start_id'])
    end_id = int(data['end_id'])
    remove_id = int(data['remove_id'])
    
    # En kısa yolu bul ve BST'yi yeniden oluştur
    path = graph.get_shortest_path(start_id, end_id)
    if not path:
        return jsonify({'error': 'Yol bulunamadı'}), 404

    # BST'yi oluştur
    bst = BinarySearchTree()
    for node_id in path:
        author_data = {
            'id': node_id,
            'name': graph.nodes[node_id].name,
            'paperCount': graph.nodes[node_id].paper_count
        }
        bst.insert(graph.nodes[node_id].paper_count, author_data)

    # Yazarı sil
    if remove_id in path:
        bst.delete(graph.nodes[remove_id].paper_count)
    else:
        return jsonify({'error': 'Silinecek yazar yolda bulunamadı'}), 404

    # BST'yi graph formatına dönüştür
    nodes = []
    edges = []
    
    def traverse_bst(node, parent_id=None, x=0, y=0, level=0):
        if node:
            node_id = len(nodes)
            nodes.append({
                'id': node.data['id'],
                'label': f"{node.data['name']}\n({node.data['paperCount']})",
                'level': level,
                'x': x,
                'y': y
            })
            
            if parent_id is not None:
                edges.append({
                    'from': parent_id,
                    'to': node.data['id'],
                })
            
            if node.left:
                traverse_bst(node.left, node.data['id'], x - 200/(level+1), y + 100, level + 1)
            if node.right:
                traverse_bst(node.right, node.data['id'], x + 200/(level+1), y + 100, level + 1)
    
    traverse_bst(bst.root)
    
    return jsonify({
        'bst': bst.inorder(),
        'nodes': nodes,
        'edges': edges
    })
@app.route('/api/most-collaborative', methods=['GET'])
def get_most_collaborative():
    """En çok işbirliği yapan yazarı bul"""
    result = graph.get_most_collaborative_author()
    if result is None:
        return jsonify({'error': 'Yazar bulunamadı'}), 404
        
    author_id, collab_count = result
    return jsonify({
        'id': author_id,
        'name': graph.nodes[author_id].name,
        'collaborationCount': collab_count
    })

@app.route('/api/shortestpath', methods=['GET'])
def get_shortest_path():
    try:
        start = request.args.get('start')
        end = request.args.get('end')

        if not start or not end:
            return jsonify({'error': 'Başlangıç ve bitiş ID\'leri gerekli'}), 400

        start_id = int(start)
        end_id = int(end)
        path, final_queue, distances = graph.get_shortest_path_with_queue(start_id, end_id)
        if not path:
            return jsonify({'error': 'Yol bulunamadı'}), 404

        # Filter out nodes with infinite distances
        filtered_queue = [node_id for node_id in final_queue if distances[node_id] != float('inf')]

        response_data = {
            'path': path,
            'authors': [graph.nodes[node_id].name for node_id in path],
            'queue': [
                {
                    'id': int(node_id),
                    'name': graph.nodes[node_id].name,
                    'distance': float(distances[node_id])
                }
                for node_id in filtered_queue
            ]
        }
        return jsonify(response_data)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)