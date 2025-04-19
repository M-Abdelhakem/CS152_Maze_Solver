from typing import Dict, Any, List
import time
from utils import Pair, make_2d_array, get_neighbors, PriorityQueueItem
from heapq import heappush, heappop

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
    
    visited = make_2d_array(size, False)
    parent = make_2d_array(size, Pair(-1, -1))
    g_score = make_2d_array(size, float('inf'))
    f_score = make_2d_array(size, float('inf'))
    exploration_order = []
    
    g_score[start.first][start.second] = 0
    f_score[start.first][start.second] = heuristic_type(start, end)
    
    open_set = []
    heappush(open_set, PriorityQueueItem(f_score[start.first][start.second], start))
    
    while open_set:
        current = heappop(open_set).item
        
        if visited[current.first][current.second]:
            continue
            
        visited[current.first][current.second] = True
        exploration_order.append([current.first, current.second])
        
        if current.first == end.first and current.second == end.second:
            # Reconstruct path
            path = []
            while current.first != -1:
                path.insert(0, current)
                current = parent[current.first][current.second]
            
            # Calculate metrics
            explored_size = sum(sum(row) for row in visited)
            frontier_size = len(open_set)
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
            tentative_g_score = g_score[current.first][current.second] + 1
            
            if tentative_g_score < g_score[neighbor.first][neighbor.second]:
                parent[neighbor.first][neighbor.second] = current
                g_score[neighbor.first][neighbor.second] = tentative_g_score
                f_score[neighbor.first][neighbor.second] = tentative_g_score + heuristic_type(neighbor, end)
                
                if not visited[neighbor.first][neighbor.second]:
                    heappush(open_set, PriorityQueueItem(f_score[neighbor.first][neighbor.second], neighbor))
    
    # Calculate metrics for no path found
    explored_size = sum(sum(row) for row in visited)
    frontier_size = len(open_set)
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