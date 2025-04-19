from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Any
import math
from queue import PriorityQueue
from algorithms.iterative_deepening import iterative_deepening
from algorithms.bidirectional import bidirectional_search
from algorithms.dfs import dfs
import time

@dataclass
class Pair:
    first: int
    second: int

class PriorityQueueItem:
    def __init__(self, priority: float, item: Pair):
        self.priority = priority
        self.item = item

    def __lt__(self, other):
        return self.priority < other.priority

def make_2d_array(size: int, default_value) -> List[List]:
    return [[default_value for _ in range(size)] for _ in range(size)]

def is_safe(x: int, y: int, size: int, blocks: List[List[bool]]) -> bool:
    return x < size and y < size and x >= 0 and y >= 0 and not blocks[x][y]

def get_neighbors(p: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int]) -> List[Pair]:
    neighbors = []
    for i in range(directions):
        x = p.first + dx[i]
        y = p.second + dy[i]
        if is_safe(x, y, size, blocks):
            neighbors.append(Pair(x, y))
    return neighbors

def bfs(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int]) -> Dict[str, Any]:
    # Special case: if start and end are the same
    if start.first == end.first and start.second == end.second:
        return {
            "path": [start],
            "exploration_order": [[start.first, start.second]],
            "metrics": {
                "explored_size": 1,
                "frontier_size": 0,
                "time_taken_ms": 0,
                "path_length": 0
            }
        }
    
    start_time = time.time()
    visited = make_2d_array(size, False)
    distance = make_2d_array(size, float('inf'))
    parent = make_2d_array(size, Pair(-1, -1))
    exploration_order = []
    
    parent[start.first][start.second] = Pair(-1, -1)
    q = [start]
    
    while q:
        p = q.pop(0)
        visited[p.first][p.second] = True
        exploration_order.append([p.first, p.second])
        
        if p.first == end.first and p.second == end.second:
            # Reconstruct path
            path = []
            current = end
            while current.first != -1:
                path.insert(0, current)
                current = parent[current.first][current.second]
                
            # Calculate metrics
            explored_size = sum(sum(row) for row in visited)
            frontier_size = len(q)
            time_taken_ms = (time.time() - start_time) * 1000
            path_length = len(path) - 1  # Subtract 1 to not count the start node
            
            return {
                "path": path,
                "exploration_order": exploration_order,
                "metrics": {
                    "explored_size": explored_size,
                    "frontier_size": frontier_size,
                    "time_taken_ms": time_taken_ms,
                    "path_length": path_length
                }
            }
            
        for i in range(directions):
            x = p.first + dx[i]
            y = p.second + dy[i]
            
            if is_safe(x, y, size, blocks) and not visited[x][y]:
                distance[x][y] = distance[p.first][p.second] + 1
                visited[x][y] = True
                parent[x][y] = p
                q.append(Pair(x, y))
    
    # Calculate metrics for no path found
    explored_size = sum(sum(row) for row in visited)
    frontier_size = len(q)
    time_taken_ms = (time.time() - start_time) * 1000
    
    return {
        "path": None,
        "exploration_order": exploration_order,
        "metrics": {
            "explored_size": explored_size,
            "frontier_size": frontier_size,
            "time_taken_ms": time_taken_ms,
            "path_length": 0
        }
    }

def dijkstra(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int]) -> Dict[str, Any]:
    # Special case: if start and end are the same
    if start.first == end.first and start.second == end.second:
        return {
            "path": [start],
            "exploration_order": [[start.first, start.second]],
            "metrics": {
                "explored_size": 1,
                "frontier_size": 0,
                "time_taken_ms": 0,
                "path_length": 0
            }
        }
    
    start_time = time.time()
    distance = make_2d_array(size, float('inf'))
    visited = make_2d_array(size, False)
    prev = make_2d_array(size, None)
    exploration_order = []
    
    distance[start.first][start.second] = 0
    pq = PriorityQueue()
    pq.put(PriorityQueueItem(0, start))
    
    while not pq.empty():
        current = pq.get().item
        
        if visited[current.first][current.second]:
            continue
            
        visited[current.first][current.second] = True
        exploration_order.append([current.first, current.second])
        
        if current.first == end.first and current.second == end.second:
            # Reconstruct path
            path = []
            while current is not None:
                path.insert(0, current)
                current = prev[current.first][current.second]
                
            # Calculate metrics
            explored_size = sum(sum(row) for row in visited)
            frontier_size = pq.qsize()
            time_taken_ms = (time.time() - start_time) * 1000
            path_length = len(path) - 1  # Subtract 1 to not count the start node
            
            return {
                "path": path,
                "exploration_order": exploration_order,
                "metrics": {
                    "explored_size": explored_size,
                    "frontier_size": frontier_size,
                    "time_taken_ms": time_taken_ms,
                    "path_length": path_length
                }
            }
            
        neighbors = get_neighbors(current, blocks, size, directions, dx, dy)
        for neighbor in neighbors:
            alt = distance[current.first][current.second] + 1
            if alt < distance[neighbor.first][neighbor.second]:
                distance[neighbor.first][neighbor.second] = alt
                prev[neighbor.first][neighbor.second] = current
                pq.put(PriorityQueueItem(alt, neighbor))
    
    # Calculate metrics for no path found
    explored_size = sum(sum(row) for row in visited)
    frontier_size = pq.qsize()
    time_taken_ms = (time.time() - start_time) * 1000
    
    return {
        "path": None,
        "exploration_order": exploration_order,
        "metrics": {
            "explored_size": explored_size,
            "frontier_size": frontier_size,
            "time_taken_ms": time_taken_ms,
            "path_length": 0
        }
    }

def get_heuristic(heuristic_type: int):
    def manhattan_distance(a: Pair, b: Pair) -> float:
        return abs(a.first - b.first) + abs(a.second - b.second)
        
    def diagonal_distance(a: Pair, b: Pair) -> float:
        dx = abs(a.first - b.first)
        dy = abs(a.second - b.second)
        return dx + dy + (math.sqrt(2) - 2) * min(dx, dy)
        
    def euclidean_distance(a: Pair, b: Pair) -> float:
        dx = a.first - b.first
        dy = a.second - b.second
        return math.sqrt(dx * dx + dy * dy)
        
    def chebyshev_distance(a: Pair, b: Pair) -> float:
        return max(abs(a.first - b.first), abs(a.second - b.second))
        
    def octile_distance(a: Pair, b: Pair) -> float:
        dx = abs(a.first - b.first)
        dy = abs(a.second - b.second)
        D = 1
        D2 = math.sqrt(2)
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
        
    def squared_euclidean_distance(a: Pair, b: Pair) -> float:
        dx = a.first - b.first
        dy = a.second - b.second
        return dx * dx + dy * dy
        
    def minkowski_distance(a: Pair, b: Pair, p: float = 10) -> float:
        dx = abs(a.first - b.first)
        dy = abs(a.second - b.second)
        return math.pow(math.pow(dx, p) + math.pow(dy, p), 1 / p)
    
    heuristics = [
        manhattan_distance,
        diagonal_distance,
        euclidean_distance,
        chebyshev_distance,
        octile_distance,
        squared_euclidean_distance,
        minkowski_distance
    ]
    
    return heuristics[heuristic_type]

def astar(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int], heuristic_type: int) -> Dict[str, Any]:
    # Special case: if start and end are the same
    if start.first == end.first and start.second == end.second:
        return {
            "path": [start],
            "exploration_order": [[start.first, start.second]],
            "metrics": {
                "explored_size": 1,
                "frontier_size": 0,
                "time_taken_ms": 0,
                "path_length": 0
            }
        }
    
    start_time = time.time()
    distance = make_2d_array(size, float('inf'))
    visited = make_2d_array(size, False)
    prev = make_2d_array(size, None)
    exploration_order = []
    
    heuristic = get_heuristic(heuristic_type)
    distance[start.first][start.second] = 0
    
    pq = PriorityQueue()
    pq.put(PriorityQueueItem(0, start))
    
    while not pq.empty():
        current = pq.get().item
        
        if visited[current.first][current.second]:
            continue
            
        visited[current.first][current.second] = True
        exploration_order.append([current.first, current.second])
        
        if current.first == end.first and current.second == end.second:
            # Reconstruct path
            path = []
            while current is not None:
                path.insert(0, current)
                current = prev[current.first][current.second]
                
            # Calculate metrics
            explored_size = sum(sum(row) for row in visited)
            frontier_size = pq.qsize()
            time_taken_ms = (time.time() - start_time) * 1000
            path_length = len(path) - 1  # Subtract 1 to not count the start node
            
            return {
                "path": path,
                "exploration_order": exploration_order,
                "metrics": {
                    "explored_size": explored_size,
                    "frontier_size": frontier_size,
                    "time_taken_ms": time_taken_ms,
                    "path_length": path_length
                }
            }
            
        neighbors = get_neighbors(current, blocks, size, directions, dx, dy)
        for neighbor in neighbors:
            alt = distance[current.first][current.second] + 1
            if alt < distance[neighbor.first][neighbor.second]:
                distance[neighbor.first][neighbor.second] = alt
                prev[neighbor.first][neighbor.second] = current
                f_score = alt + heuristic(neighbor, end)
                pq.put(PriorityQueueItem(f_score, neighbor))
    
    # Calculate metrics for no path found
    explored_size = sum(sum(row) for row in visited)
    frontier_size = pq.qsize()
    time_taken_ms = (time.time() - start_time) * 1000
    
    return {
        "path": None,
        "exploration_order": exploration_order,
        "metrics": {
            "explored_size": explored_size,
            "frontier_size": frontier_size,
            "time_taken_ms": time_taken_ms,
            "path_length": 0
        }
    } 