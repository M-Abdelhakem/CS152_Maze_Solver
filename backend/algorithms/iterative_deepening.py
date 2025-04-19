from typing import Dict, Any, List, Optional
import time
from utils import Pair, make_2d_array, get_neighbors

def iterative_deepening(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int]) -> Dict[str, Any]:
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
    total_frontier = 0
    exploration_order = []
    
    def depth_limited_dfs(current: Pair, depth: int, visited: List[List[bool]], parent: List[List[Pair]], 
                         current_exploration: List[List[int]]) -> bool:
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
    
    max_depth = size * size  # Maximum possible depth
    for depth in range(1, max_depth + 1):
        visited = make_2d_array(size, False)
        parent = make_2d_array(size, Pair(-1, -1))
        current_exploration = []
        
        # Reset visited for this iteration
        for i in range(size):
            for j in range(size):
                visited[i][j] = False
        
        # Run DFS with current depth limit
        if depth_limited_dfs(start, depth, visited, parent, current_exploration):
            # Path found, reconstruct it
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
            
            # Add this iteration's exploration to the total
            exploration_order.extend(current_exploration)
            
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
        
        # Add this iteration's exploration to the total
        exploration_order.extend(current_exploration)
        total_explored += sum(sum(row) for row in visited)
    
    # No path found after trying all depths
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