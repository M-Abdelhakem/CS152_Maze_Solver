from typing import Dict, Any, List, Optional
import time
from collections import deque
from utils import Pair, make_2d_array, get_neighbors

def bidirectional_search(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int]) -> Dict[str, Any]:
    """Implements the Bidirectional Search algorithm for pathfinding.
    
    Bidirectional Search performs two simultaneous breadth-first searches - one from the start
    node and one from the goal node. The algorithm terminates when the two searches meet at
    an intersection point. This approach can be significantly faster than a single BFS as it
    reduces the search space by exploring from both ends.
    
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
                - explored_size: Total number of nodes explored in both directions
                - frontier_size: Total size of both forward and backward frontiers
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
                "path_length": 0,
                "total_cost": 0
            }
        }
    
    start_time = time.time()
    
    # Initialize data structures for forward search
    visited_forward = make_2d_array(size, False)
    parent_forward = make_2d_array(size, Pair(-1, -1))
    
    # Initialize data structures for backward search
    visited_backward = make_2d_array(size, False)
    parent_backward = make_2d_array(size, Pair(-1, -1))
    
    # Initialize queues
    queue_forward = deque([start])
    queue_backward = deque([end])
    
    # Mark start and end as visited
    visited_forward[start.first][start.second] = True
    visited_backward[end.first][end.second] = True
    
    # Track exploration order
    exploration_order = []
    
    # Track intersection point
    intersection = None
    
    while queue_forward and queue_backward:
        # Forward search step
        if queue_forward:
            current_forward = queue_forward.popleft()
            exploration_order.append([current_forward.first, current_forward.second])
            
            # Check if we've found an intersection
            if visited_backward[current_forward.first][current_forward.second]:
                intersection = current_forward
                break
                
            # Explore neighbors in forward direction
            neighbors = get_neighbors(current_forward, blocks, size, directions, dx, dy)
            for neighbor in neighbors:
                if not visited_forward[neighbor.first][neighbor.second]:
                    visited_forward[neighbor.first][neighbor.second] = True
                    parent_forward[neighbor.first][neighbor.second] = current_forward
                    queue_forward.append(neighbor)
        
        # Backward search step
        if queue_backward and not intersection:
            current_backward = queue_backward.popleft()
            exploration_order.append([current_backward.first, current_backward.second])
            
            # Check if we've found an intersection
            if visited_forward[current_backward.first][current_backward.second]:
                intersection = current_backward
                break
                
            # Explore neighbors in backward direction
            neighbors = get_neighbors(current_backward, blocks, size, directions, dx, dy)
            for neighbor in neighbors:
                if not visited_backward[neighbor.first][neighbor.second]:
                    visited_backward[neighbor.first][neighbor.second] = True
                    parent_backward[neighbor.first][neighbor.second] = current_backward
                    queue_backward.append(neighbor)
    
    # Calculate metrics
    explored_size = sum(sum(row) for row in visited_forward) + sum(sum(row) for row in visited_backward)
    frontier_size = len(queue_forward) + len(queue_backward)
    time_taken_ms = (time.time() - start_time) * 1000
    
    if intersection:
        # Reconstruct path from start to intersection
        path_forward = []
        current = intersection
        total_cost = 0
        while current.first != -1:
            path_forward.insert(0, current)
            if parent_forward[current.first][current.second].first != -1:
                total_cost += 1  # Each step has a cost of 1
            current = parent_forward[current.first][current.second]
        
        # Reconstruct path from intersection to end (excluding intersection)
        path_backward = []
        current = parent_backward[intersection.first][intersection.second]
        while current.first != -1:
            path_backward.insert(0, current)  # Insert at beginning to properly reverse
            if parent_backward[current.first][current.second].first != -1:
                total_cost += 1  # Each step has a cost of 1
            current = parent_backward[current.first][current.second]
        
        # Reverse the backward path and append to forward path
        path_backward.reverse()
        path = path_forward + path_backward
        path_length = len(path) - 1  # Subtract 1 to not count the start node
        
        return {
            "path": path,
            "exploration_order": exploration_order,
            "metrics": {
                "explored_size": explored_size,
                "frontier_size": frontier_size,
                "time_taken_ms": time_taken_ms,
                "path_length": path_length,
                "total_cost": total_cost
            }
        }
    
    # No path found
    return {
        "path": None,
        "exploration_order": exploration_order,
        "metrics": {
            "explored_size": explored_size,
            "frontier_size": frontier_size,
            "time_taken_ms": time_taken_ms,
            "path_length": 0,
            "total_cost": 0
        }
    } 