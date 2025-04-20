import random
import math
from typing import List, Dict, Any, Optional, Tuple
from utils import Pair
import time

class Node:
    def __init__(self, x: int, y: int, parent: Optional['Node'] = None):
        self.x = x
        self.y = y
        self.parent = parent

def rrt(
    start: Pair,
    end: Pair,
    blocks: List[List[bool]],
    size: int,
    directions: int,
    dx: List[int],
    dy: List[int],
    step_size: float = 1.0,
    max_iterations: int = 1000,
    goal_sample_rate: float = 0.1
) -> Dict[str, Any]:
    start_time = time.time()
    exploration_order = []
    metrics = {
        "explored_size": 0,
        "frontier_size": 0,
        "time_taken_ms": 0,
        "path_length": 0
    }

    # Initialize the tree with the start node
    start_node = Node(start.first, start.second)
    nodes = [start_node]
    
    def is_safe(x: int, y: int) -> bool:
        return 0 <= x < size and 0 <= y < size and not blocks[x][y]

    def get_distance(node1: Node, node2: Node) -> float:
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    def get_nearest_node(x: float, y: float) -> Node:
        min_dist = float('inf')
        nearest = None
        for node in nodes:
            dist = math.sqrt((node.x - x) ** 2 + (node.y - y) ** 2)
            if dist < min_dist:
                min_dist = dist
                nearest = node
        return nearest

    def get_valid_directions() -> List[Tuple[int, int]]:
        if directions == 8:
            # 8 directions: horizontal, vertical, and diagonal
            return [
                (1, 0), (1, 1), (0, 1), (-1, 1),
                (-1, 0), (-1, -1), (0, -1), (1, -1)
            ]
        else:
            # 4 directions: horizontal and vertical only
            return [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def steer(from_node: Node, to_x: float, to_y: float) -> Tuple[int, int]:
        # Calculate the direction vector
        dx = to_x - from_node.x
        dy = to_y - from_node.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist <= step_size:
            return int(to_x), int(to_y)
        
        # Get valid directions
        valid_dirs = get_valid_directions()
        
        # Find the best direction
        best_dir = None
        min_angle_diff = float('inf')
        
        # Normalize the target direction vector
        if dist > 0:
            nx, ny = dx / dist, dy / dist
        else:
            return from_node.x, from_node.y
        
        for dir_x, dir_y in valid_dirs:
            # Calculate the normalized direction vector
            dir_len = math.sqrt(dir_x**2 + dir_y**2)
            dir_nx, dir_ny = dir_x / dir_len, dir_y / dir_len
            
            # Calculate the dot product to find the cosine of the angle
            dot_product = nx * dir_nx + ny * dir_ny
            
            # Calculate the angle difference (in radians)
            angle_diff = math.acos(max(-1.0, min(1.0, dot_product)))
            
            if angle_diff < min_angle_diff:
                min_angle_diff = angle_diff
                best_dir = (dir_x, dir_y)
        
        if best_dir:
            dir_x, dir_y = best_dir
            # Normalize the step size based on direction
            dir_len = math.sqrt(dir_x**2 + dir_y**2)
            move_x = step_size * dir_x / dir_len
            move_y = step_size * dir_y / dir_len
            
            return int(round(from_node.x + move_x)), int(round(from_node.y + move_y))
        
        return from_node.x, from_node.y

    def is_path_free(node1: Node, x: int, y: int) -> bool:
        # Check if the path between node1 and (x,y) is free of obstacles
        x1, y1 = node1.x, node1.y
        x2, y2 = x, y
        
        # Get the direction vector
        dx = x2 - x1
        dy = y2 - y1
        
        # Determine if this is a diagonal move
        is_diagonal = dx != 0 and dy != 0
        
        # Check if start and end points are valid
        if not is_safe(x1, y1) or not is_safe(x2, y2):
            return False
        
        # For diagonal movement, check the direct path
        if is_diagonal:
            # Calculate the number of steps to check along the path
            steps = max(abs(dx), abs(dy))
            
            # Check points along the path
            for i in range(1, steps + 1):
                t = i / steps
                check_x = int(round(x1 + t * dx))
                check_y = int(round(y1 + t * dy))
                
                if not is_safe(check_x, check_y):
                    return False
                
                # For diagonal moves, also check the orthogonal neighbors to avoid corner cutting
                if directions == 8:
                    # Check if the movement is diagonal
                    if i < steps:  # Skip the final point as it's already checked
                        # Check orthogonal neighbors to prevent corner cutting
                        if not is_safe(check_x, y1) or not is_safe(x1, check_y):
                            return False
        else:
            # For orthogonal movement, check a straight line
            steps = max(abs(dx), abs(dy))
            for i in range(1, steps):
                t = i / steps
                check_x = int(round(x1 + t * dx))
                check_y = int(round(y1 + t * dy))
                
                if not is_safe(check_x, check_y):
                    return False
                    
        return True

    for i in range(max_iterations):
        # Random sampling
        if random.random() < goal_sample_rate:
            sample_x, sample_y = end.first, end.second
        else:
            sample_x = random.randint(0, size - 1)
            sample_y = random.randint(0, size - 1)

        # Find nearest node
        nearest_node = get_nearest_node(sample_x, sample_y)
        
        # Steer towards the sample
        new_x, new_y = steer(nearest_node, sample_x, sample_y)
        
        # Check if the new position is different from the nearest node
        if new_x == nearest_node.x and new_y == nearest_node.y:
            continue
        
        # Check if path is free
        if is_path_free(nearest_node, new_x, new_y):
            new_node = Node(new_x, new_y, nearest_node)
            nodes.append(new_node)
            exploration_order.append([new_node.x, new_node.y])
            
            # Check if we reached the goal
            if get_distance(new_node, Node(end.first, end.second)) <= step_size:
                # Reconstruct path
                path = []
                current = new_node
                while current is not None:
                    path.append(Pair(current.x, current.y))
                    current = current.parent
                path.reverse()
                
                metrics["explored_size"] = len(nodes)
                metrics["frontier_size"] = 0  # RRT doesn't maintain a frontier
                metrics["time_taken_ms"] = (time.time() - start_time) * 1000
                metrics["path_length"] = len(path)
                
                return {
                    "path": path,
                    "exploration_order": exploration_order,
                    "metrics": metrics
                }

    # If no path found
    metrics["explored_size"] = len(nodes)
    metrics["frontier_size"] = 0
    metrics["time_taken_ms"] = (time.time() - start_time) * 1000
    metrics["path_length"] = 0
    
    return {
        "path": None,
        "exploration_order": exploration_order,
        "metrics": metrics
    }