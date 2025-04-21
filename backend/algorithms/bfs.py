from typing import Dict, Any, List
import time
from utils import Pair, make_2d_array, get_neighbors

def bfs(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int]) -> Dict[str, Any]:
    """Implements the Breadth-First Search (BFS) algorithm for pathfinding.
    
    BFS explores all nodes at the current depth before moving to nodes at the next depth level.
    It guarantees the shortest path in terms of number of steps when all steps have equal cost.
    
    Args:
        start (Pair): Starting position coordinates (x, y)
        end (Pair): Goal position coordinates (x, y)
        blocks (List[List[bool]]): 2D grid representing obstacles (True for blocked cells)
        size (int): Size of the grid (assuming square grid)
        directions (int): Number of possible movement directions (4 or 8)
        dx (List[int]): List of x-direction movements
        dy (List[int]): List of y-direction movements
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - path: List of Pair objects representing the found path, or None if no path exists
            - exploration_order: List of coordinates showing the order of exploration
            - metrics: Dictionary containing performance metrics:
                - explored_size: Number of nodes explored
                - frontier_size: Size of the frontier (queue)
                - time_taken_ms: Time taken to find the path in milliseconds
                - path_length: Length of the found path (0 if no path found)
    """
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
    parent = make_2d_array(size, Pair(-1, -1))
    queue = [start]
    visited[start.first][start.second] = True
    exploration_order = [[start.first, start.second]]
    
    while queue:
        current = queue.pop(0)
        
        if current.first == end.first and current.second == end.second:
            # Reconstruct path
            path = []
            while current.first != -1:
                path.insert(0, current)
                current = parent[current.first][current.second]
            
            # Calculate metrics
            explored_size = sum(sum(row) for row in visited)
            frontier_size = len(queue)
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
            if not visited[neighbor.first][neighbor.second]:
                visited[neighbor.first][neighbor.second] = True
                parent[neighbor.first][neighbor.second] = current
                queue.append(neighbor)
                exploration_order.append([neighbor.first, neighbor.second])
    
    # Calculate metrics for no path found
    explored_size = sum(sum(row) for row in visited)
    frontier_size = len(queue)
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