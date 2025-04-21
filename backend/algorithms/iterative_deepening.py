from typing import Dict, Any, List, Optional
import time
from utils import Pair, make_2d_array, get_neighbors

def iterative_deepening(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int]) -> Dict[str, Any]:
    """Implements the Iterative Deepening Depth-First Search (IDDFS) algorithm for pathfinding.
    
    IDDFS combines the space efficiency of DFS with the completeness of BFS. It performs
    a series of depth-limited DFS searches, gradually increasing the depth limit until
    the goal is found or a maximum reasonable depth is reached.
    
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
                - explored_size: Total number of nodes explored across all depth iterations
                - frontier_size: Always 0 as IDDFS doesn't maintain a frontier
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
    total_explored = 0
    exploration_order = []
    max_reasonable_depth = size * 2  # A reasonable maximum depth
    
    def depth_limited_dfs(current: Pair, depth: int, visited: List[List[bool]], parent: List[List[Pair]], 
                         current_exploration: List[List[int]]) -> bool:
        """Helper function that performs a depth-limited DFS search.
        
        Args:
            current (Pair): Current position being explored
            depth (int): Remaining depth to explore
            visited (List[List[bool]]): 2D array tracking visited nodes
            parent (List[List[Pair]]): 2D array tracking parent nodes for path reconstruction
            current_exploration (List[List[int]]): List to track exploration order for current depth
            
        Returns:
            bool: True if path to goal is found within depth limit, False otherwise
        """
        if depth < 0:
            return False
            
        visited[current.first][current.second] = True
        current_exploration.append([current.first, current.second])
        
        if current.first == end.first and current.second == end.second:
            return True
            
        if depth == 0:
            return False
            
        neighbors = get_neighbors(current, blocks, size, directions, dx, dy)
        for neighbor in neighbors:
            if not visited[neighbor.first][neighbor.second]:
                parent[neighbor.first][neighbor.second] = current
                if depth_limited_dfs(neighbor, depth - 1, visited, parent, current_exploration):
                    return True
                    
        return False
    
    for depth in range(1, max_reasonable_depth + 1):
        # Create new visited and parent arrays for each depth iteration
        visited = make_2d_array(size, False)
        parent = make_2d_array(size, Pair(-1, -1))
        current_exploration = []
        
        # Run DFS with current depth limit
        if depth_limited_dfs(start, depth, visited, parent, current_exploration):
            # Path found, reconstruct it
            path = []
            current = end
            while current.first != -1:
                path.insert(0, current)
                current = parent[current.first][current.second]
            
            # Calculate metrics
            explored_size = total_explored + sum(sum(row) for row in visited)
            time_taken_ms = (time.time() - start_time) * 1000
            path_length = len(path) - 1  # Subtract 1 to not count the start node
            
            # Add this iteration's exploration to the total
            exploration_order.extend(current_exploration)
            
            return {
                "path": path,
                "exploration_order": exploration_order,
                "metrics": {
                    "explored_size": explored_size,
                    "frontier_size": 0,  # No frontier in IDDFS
                    "time_taken_ms": time_taken_ms,
                    "path_length": path_length
                }
            }
        
        # Add this iteration's exploration to the total
        exploration_order.extend(current_exploration)
        total_explored += sum(sum(row) for row in visited)
    
    # No path found after trying all reasonable depths
    time_taken_ms = (time.time() - start_time) * 1000
    
    return {
        "path": None,
        "exploration_order": exploration_order,
        "metrics": {
            "explored_size": total_explored,
            "frontier_size": 0,
            "time_taken_ms": time_taken_ms,
            "path_length": 0
        }
    } 