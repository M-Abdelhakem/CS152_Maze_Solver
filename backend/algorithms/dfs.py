from typing import Dict, Any, List
import time
import sys
from utils import Pair, make_2d_array, get_neighbors

def dfs(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int], max_depth: int = None) -> Dict[str, Any]:
    """Implements the Depth-First Search (DFS) algorithm for pathfinding.
    
    DFS explores as far as possible along each branch before backtracking. It uses recursion
    with a maximum depth limit to prevent stack overflow. While it may not find the shortest
    path, it can be more memory efficient than BFS for certain types of mazes.
    
    Args:
        start (Pair): Starting position coordinates (x, y)
        end (Pair): Goal position coordinates (x, y)
        blocks (List[List[bool]]): 2D grid representing obstacles (True for blocked cells)
        size (int): Size of the grid (assuming square grid)
        directions (int): Number of possible movement directions (4 or 8)
        dx (List[int]): List of x-direction movements
        dy (List[int]): List of y-direction movements
        max_depth (int, optional): Maximum recursion depth. Defaults to size * size
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - path: List of Pair objects representing the found path, or None if no path exists
            - exploration_order: List of coordinates showing the order of exploration
            - metrics: Dictionary containing performance metrics:
                - explored_size: Number of nodes explored
                - frontier_size: Always 0 as DFS doesn't maintain a frontier
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
    
    # Set default max depth to avoid excessive recursion
    if max_depth is None:
        max_depth = size * size  # Default max depth
    
    # Get current recursion limit and set a higher one if needed
    current_limit = sys.getrecursionlimit()
    if max_depth > current_limit:
        sys.setrecursionlimit(max_depth + 100)  # Add some buffer
    
    visited = make_2d_array(size, False)
    parent = make_2d_array(size, Pair(-1, -1))
    exploration_order = []
    
    def dfs_recursive(current: Pair, depth: int) -> bool:
        """Helper function that performs the recursive DFS search.
        
        Args:
            current (Pair): Current position being explored
            depth (int): Current depth in the recursion
            
        Returns:
            bool: True if path to goal is found, False otherwise
        """
        if depth <= 0:
            return False
            
        visited[current.first][current.second] = True
        exploration_order.append([current.first, current.second])
        
        if current.first == end.first and current.second == end.second:
            return True
            
        neighbors = get_neighbors(current, blocks, size, directions, dx, dy)
        for neighbor in neighbors:
            if not visited[neighbor.first][neighbor.second]:
                parent[neighbor.first][neighbor.second] = current
                if dfs_recursive(neighbor, depth - 1):
                    return True
                    
        return False
    
    # Start DFS from the start position with limited depth
    if dfs_recursive(start, max_depth):
        # Reconstruct path
        path = []
        current = end
        while current.first != -1:
            path.insert(0, current)
            current = parent[current.first][current.second]
        
        # Calculate metrics
        explored_size = sum(sum(row) for row in visited)
        frontier_size = 0  # DFS doesn't maintain a frontier
        time_taken_ms = (time.time() - start_time) * 1000
        path_length = len(path) - 1  # Subtract 1 to not count the start node
        
        # Reset recursion limit if we changed it
        if max_depth > current_limit:
            sys.setrecursionlimit(current_limit)
        
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
    
    # Calculate metrics for no path found
    explored_size = sum(sum(row) for row in visited)
    frontier_size = 0  # DFS doesn't maintain a frontier
    time_taken_ms = (time.time() - start_time) * 1000
    
    # Reset recursion limit if we changed it
    if max_depth > current_limit:
        sys.setrecursionlimit(current_limit)
    
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