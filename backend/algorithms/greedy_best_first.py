from typing import Dict, Any, List
import time
from queue import PriorityQueue
from utils import Pair, make_2d_array, get_neighbors, get_heuristic, PriorityQueueItem

def greedy_best_first(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int], heuristic_type: str = "manhattan", weights: List[List[int]] = None, is_weighted: bool = False) -> Dict[str, Any]:
    """Implements the Greedy Best-First Search algorithm for pathfinding.
    
    Greedy Best-First Search uses a heuristic function to estimate the distance to the goal
    and always expands the node that appears to be closest to the goal. When is_weighted is True,
    it considers cell weights in the path selection, though it may not find the optimal path.
    
    Args:
        start (Pair): Starting position coordinates (x, y)
        end (Pair): Goal position coordinates (x, y)
        blocks (List[List[bool]]): 2D grid representing obstacles (True for blocked cells)
        size (int): Size of the grid (assuming square grid)
        directions (int): Number of possible movement directions (4 or 8)
        dx (List[int]): List of x-direction movements
        dy (List[int]): List of y-direction movements
        heuristic_type (str, optional): Type of heuristic to use ("manhattan", "euclidean", etc.). Defaults to "manhattan"
        weights (List[List[int]], optional): 2D grid of cell weights. Defaults to None.
        is_weighted (bool, optional): Whether to use weights. Defaults to False.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - path: List of Pair objects representing the found path, or None if no path exists
            - exploration_order: List of coordinates showing the order of exploration
            - metrics: Dictionary containing performance metrics:
                - explored_size: Number of nodes explored
                - frontier_size: Size of the frontier (priority queue)
                - time_taken_ms: Time taken to find the path in milliseconds
                - path_length: Length of the found path (0 if no path found)
                - total_cost: Total cost of the path (sum of weights)
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
    visited = make_2d_array(size, False)
    parent = make_2d_array(size, Pair(-1, -1))
    pq = PriorityQueue()
    heuristic_func = get_heuristic(heuristic_type)
    
    # Calculate initial score considering weights if enabled
    initial_score = heuristic_func(start, end)
    if is_weighted and weights:
        initial_score += weights[start.first][start.second]
    pq.put(PriorityQueueItem(initial_score, start))
    
    exploration_order = []
    
    # Mark start as in frontier
    in_frontier = make_2d_array(size, False)
    in_frontier[start.first][start.second] = True
    
    while not pq.empty():
        current = pq.get().item
        
        # Skip if already visited
        if visited[current.first][current.second]:
            continue
            
        # Mark as visited and add to exploration order
        visited[current.first][current.second] = True
        in_frontier[current.first][current.second] = False
        exploration_order.append([current.first, current.second])
        
        if current.first == end.first and current.second == end.second:
            # Reconstruct path
            path = []
            total_cost = 0
            while current.first != -1:
                path.insert(0, current)
                if parent[current.first][current.second].first != -1:
                    # Add the weight of the current cell to total cost
                    if is_weighted and weights:
                        total_cost += weights[current.first][current.second]
                    else:
                        total_cost += 1
                current = parent[current.first][current.second]
            
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
                    "path_length": path_length,
                    "total_cost": total_cost
                }
            }
        
        neighbors = get_neighbors(current, blocks, size, directions, dx, dy)
        for neighbor in neighbors:
            if not visited[neighbor.first][neighbor.second]:
                parent[neighbor.first][neighbor.second] = current
                
                # Calculate score considering weights if enabled
                score = heuristic_func(neighbor, end)
                if is_weighted and weights:
                    score += weights[neighbor.first][neighbor.second]
                
                # Add to frontier if not already there
                if not in_frontier[neighbor.first][neighbor.second]:
                    pq.put(PriorityQueueItem(score, neighbor))
                    in_frontier[neighbor.first][neighbor.second] = True
    
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
            "path_length": 0,
            "total_cost": 0
        }
    }