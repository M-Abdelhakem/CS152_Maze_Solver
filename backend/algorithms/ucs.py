from typing import Dict, Any, List
import time
from queue import PriorityQueue
from utils import Pair, make_2d_array, get_neighbors, PriorityQueueItem

def ucs(start: Pair, end: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int], weights: List[List[int]] = None, is_weighted: bool = False) -> Dict[str, Any]:
    """Implements Uniform Cost Search (UCS) algorithm for pathfinding.
    
    UCS is a graph search algorithm that finds the path with minimum total cost from start to goal.
    It expands the least-cost unexpanded node first, making it optimal for finding the minimum-cost path.
    When is_weighted is True, it uses the provided weights to find the path with minimum total cost.
    
    Args:
        start (Pair): Starting position coordinates (x, y)
        end (Pair): Goal position coordinates (x, y)
        blocks (List[List[bool]]): 2D grid representing obstacles (True for blocked cells)
        size (int): Size of the grid (assuming square grid)
        directions (int): Number of possible movement directions (4 or 8)
        dx (List[int]): List of x-direction movements
        dy (List[int]): List of y-direction movements
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
    cost = make_2d_array(size, float('inf'))
    pq = PriorityQueue()
    pq.put(PriorityQueueItem(0, start))
    cost[start.first][start.second] = 0
    exploration_order = []
    
    # Mark start as in frontier
    in_frontier = make_2d_array(size, False)
    in_frontier[start.first][start.second] = True
    
    while not pq.empty():
        current = pq.get().item
        in_frontier[current.first][current.second] = False
        
        # Skip if we've already visited this node (can happen due to multiple entries in PQ)
        if visited[current.first][current.second]:
            continue
        
        visited[current.first][current.second] = True
        exploration_order.append([current.first, current.second])
        
        if current.first == end.first and current.second == end.second:
            # Goal reached - reconstruct path and return results
            path = reconstruct_path(parent, end)
            return create_result(path, exploration_order, visited, pq, start_time, cost[end.first][end.second])
        
        neighbors = get_neighbors(current, blocks, size, directions, dx, dy)
        for neighbor in neighbors:
            if not visited[neighbor.first][neighbor.second]:
                # Calculate new cost
                step_cost = weights[neighbor.first][neighbor.second] if is_weighted and weights else 1
                new_cost = cost[current.first][current.second] + step_cost
                
                # Update if we found a better path
                if new_cost < cost[neighbor.first][neighbor.second]:
                    cost[neighbor.first][neighbor.second] = new_cost
                    parent[neighbor.first][neighbor.second] = current
                    
                    # Add to frontier if not already there
                    if not in_frontier[neighbor.first][neighbor.second]:
                        pq.put(PriorityQueueItem(new_cost, neighbor))
                        in_frontier[neighbor.first][neighbor.second] = True
    
    # No path found
    return create_result(None, exploration_order, visited, pq, start_time, 0)

def reconstruct_path(parent: List[List[Pair]], end: Pair) -> List[Pair]:
    """Reconstructs the path from start to end using the parent matrix.
    
    Args:
        parent (List[List[Pair]]): 2D grid of parent pointers
        end (Pair): Goal position coordinates (x, y)
    
    Returns:
        List[Pair]: List of coordinates representing the path from start to end
    """
    path = []
    current = end
    
    while current.first != -1:
        path.insert(0, current)
        current = parent[current.first][current.second]
        
    return path

def create_result(path: List[Pair], exploration_order: List[List[int]], 
                 visited: List[List[bool]], pq: PriorityQueue, 
                 start_time: float, total_cost: float) -> Dict[str, Any]:
    """Creates the standardized result dictionary.
    
    Args:
        path (List[Pair]): The found path, or None if no path exists
        exploration_order (List[List[int]]): Order of node exploration
        visited (List[List[bool]]): 2D grid of visited flags
        pq (PriorityQueue): Current frontier queue
        start_time (float): Time when search started
        total_cost (float): Total path cost
    
    Returns:
        Dict[str, Any]: Standardized result dictionary
    """
    # Calculate metrics
    explored_size = sum(sum(row) for row in visited)
    frontier_size = pq.qsize()
    time_taken_ms = (time.time() - start_time) * 1000
    path_length = len(path) - 1 if path else 0  # Subtract 1 to not count the start node
    
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