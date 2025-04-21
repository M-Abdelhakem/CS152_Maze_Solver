from typing import Dict, Any, List
import time
from utils import Pair, make_2d_array, get_neighbors, get_heuristic

def local_beam_search(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int], beam_width: int = 5, heuristic_type: int = 0) -> Dict[str, Any]:
    """Implements the Local Beam Search algorithm for pathfinding.
    
    Local Beam Search is a heuristic search algorithm that maintains a fixed number of
    best states (beam width) at each level of the search. It's similar to BFS but only
    keeps the most promising nodes based on a heuristic function. This makes it more
    memory efficient than BFS while still being guided towards the goal.
    
    Args:
        start (Pair): Starting position coordinates (x, y)
        end (Pair): Goal position coordinates (x, y)
        blocks (List[List[bool]]): 2D grid representing obstacles (True for blocked cells)
        size (int): Size of the grid (assuming square grid)
        directions (int): Number of possible movement directions (4 or 8)
        dx (List[int]): List of x-direction movements
        dy (List[int]): List of y-direction movements
        beam_width (int, optional): Number of states to maintain at each level. Defaults to 5
        heuristic_type (int, optional): Type of heuristic function to use. Defaults to 0
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - path: List of Pair objects representing the found path, or None if no path exists
            - exploration_order: List of coordinates showing the order of exploration
            - metrics: Dictionary containing performance metrics:
                - explored_size: Number of nodes explored
                - frontier_size: Size of the current beam
                - time_taken_ms: Time taken to find the path in milliseconds
                - path_length: Length of the found path (0 if no path found)
    """
    # Validate beam_width
    if beam_width < 1:
        beam_width = 1
    elif beam_width > 20:  # Set a reasonable upper limit
        beam_width = 20
    
    # Get appropriate heuristic function
    heuristic = get_heuristic(heuristic_type)
    
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
    
    # Early exit: Check if end is a direct neighbor of start
    initial_neighbors = get_neighbors(start, blocks, size, directions, dx, dy)
    for neighbor in initial_neighbors:
        if neighbor.first == end.first and neighbor.second == end.second:
            return {
                "path": [start, end],
                "exploration_order": [[start.first, start.second], [end.first, end.second]],
                "metrics": {
                    "explored_size": 2,
                    "frontier_size": len(initial_neighbors) - 1,  # All neighbors except the end
                    "time_taken_ms": 0,
                    "path_length": 1
                }
            }
    
    start_time = time.time()
    visited = make_2d_array(size, False)
    parent = make_2d_array(size, Pair(-1, -1))
    exploration_order = []
    
    # Initialize with start node
    current_level = [start]
    visited[start.first][start.second] = True
    exploration_order.append([start.first, start.second])
    
    while current_level:
        # Generate all neighbors for current level
        all_neighbors = []
        
        for current in current_level:
            neighbors = get_neighbors(current, blocks, size, directions, dx, dy)
            for neighbor in neighbors:
                if not visited[neighbor.first][neighbor.second]:
                    visited[neighbor.first][neighbor.second] = True
                    parent[neighbor.first][neighbor.second] = current
                    exploration_order.append([neighbor.first, neighbor.second])
                    all_neighbors.append(neighbor)
                    
                    # Check if we found the goal
                    if neighbor.first == end.first and neighbor.second == end.second:
                        # Reconstruct path
                        path = []
                        current = end
                        while current.first != -1:
                            path.insert(0, current)
                            current = parent[current.first][current.second]
                        
                        # Calculate metrics
                        explored_size = sum(sum(row) for row in visited)
                        frontier_size = len(all_neighbors)
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
        
        # If no neighbors found, we're stuck
        if not all_neighbors:
            break
            
        # Score all neighbors using the specified heuristic
        scored_neighbors = []
        for neighbor in all_neighbors:
            score = heuristic(neighbor, end)
            scored_neighbors.append((score, neighbor))
        
        # Sort by score and take top beam_width neighbors
        scored_neighbors.sort(key=lambda x: x[0])
        current_level = [neighbor for _, neighbor in scored_neighbors[:beam_width]]
    
    # Calculate metrics for no path found
    explored_size = sum(sum(row) for row in visited)
    frontier_size = len(current_level)
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