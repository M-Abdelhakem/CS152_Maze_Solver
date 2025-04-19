from dataclasses import dataclass
from typing import List, Dict, Any, Callable
import math

@dataclass
class Pair:
    first: int
    second: int

class PriorityQueueItem:
    def __init__(self, priority: float, item: Pair):
        self.priority = priority
        self.item = item

    def __lt__(self, other):
        return self.priority < other.priority

def make_2d_array(size: int, default_value) -> List[List]:
    return [[default_value for _ in range(size)] for _ in range(size)]

def is_safe(x: int, y: int, size: int, blocks: List[List[bool]]) -> bool:
    return x < size and y < size and x >= 0 and y >= 0 and not blocks[x][y]

def get_neighbors(p: Pair, blocks: List[List[bool]], size: int, directions: int, dx: List[int], dy: List[int]) -> List[Pair]:
    neighbors = []
    for i in range(directions):
        x = p.first + dx[i]
        y = p.second + dy[i]
        if is_safe(x, y, size, blocks):
            neighbors.append(Pair(x, y))
    return neighbors

def get_heuristic(heuristic_type: int) -> Callable[[Pair, Pair], float]:
    def manhattan_distance(a: Pair, b: Pair) -> float:
        return abs(a.first - b.first) + abs(a.second - b.second)
        
    def diagonal_distance(a: Pair, b: Pair) -> float:
        dx = abs(a.first - b.first)
        dy = abs(a.second - b.second)
        return dx + dy + (math.sqrt(2) - 2) * min(dx, dy)
        
    def euclidean_distance(a: Pair, b: Pair) -> float:
        dx = a.first - b.first
        dy = a.second - b.second
        return math.sqrt(dx * dx + dy * dy)
        
    def chebyshev_distance(a: Pair, b: Pair) -> float:
        return max(abs(a.first - b.first), abs(a.second - b.second))
        
    def octile_distance(a: Pair, b: Pair) -> float:
        dx = abs(a.first - b.first)
        dy = abs(a.second - b.second)
        D = 1
        D2 = math.sqrt(2)
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
        
    def squared_euclidean_distance(a: Pair, b: Pair) -> float:
        dx = a.first - b.first
        dy = a.second - b.second
        return dx * dx + dy * dy
    
    heuristics = [
        manhattan_distance,
        diagonal_distance,
        euclidean_distance,
        chebyshev_distance,
        octile_distance,
        squared_euclidean_distance
    ]
    
    return heuristics[heuristic_type]

# Direction constants
DX_4D = [0, 1, 0, -1]
DY_4D = [1, 0, -1, 0]
DX_8D = [0, 1, 1, 1, 0, -1, -1, -1]
DY_8D = [1, 1, 0, -1, -1, -1, 0, 1] 