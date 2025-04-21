from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from maze_solver import Pair, bfs, dfs, dijkstra, astar, iterative_deepening, bidirectional_search, local_beam_search, rrt, greedy_best_first

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Direction constants
DX_4D = [0, 1, 0, -1]
DY_4D = [1, 0, -1, 0]
DX_8D = [0, 1, 1, 1, 0, -1, -1, -1]
DY_8D = [1, 1, 0, -1, -1, -1, 0, 1]

class SolveRequest(BaseModel):
    start: List[int]
    end: List[int]
    blocks: List[List[bool]]
    size: int
    directions: int
    algorithm: str
    heuristic_type: Optional[int] = 0
    beam_width: Optional[int] = 5

class SolveResponse(BaseModel):
    path: Optional[List[List[int]]]
    exploration_order: List[List[int]]
    error: Optional[str] = None
    metrics: dict

@app.post("/solve", response_model=SolveResponse)
async def solve_maze(request: SolveRequest):
    try:
        start = Pair(request.start[0], request.start[1])
        end = Pair(request.end[0], request.end[1])
        
        dx = DX_8D if request.directions == 8 else DX_4D
        dy = DY_8D if request.directions == 8 else DY_4D
        
        result = None
        if request.algorithm == "bfs":
            result = bfs(start, end, request.blocks, request.size, request.directions, dx, dy)
        elif request.algorithm == "dfs":
            result = dfs(start, end, request.blocks, request.size, request.directions, dx, dy)
        elif request.algorithm == "dijkstra":
            result = dijkstra(start, end, request.blocks, request.size, request.directions, dx, dy)
        elif request.algorithm == "astar":
            result = astar(start, end, request.blocks, request.size, request.directions, dx, dy, request.heuristic_type)
        elif request.algorithm == "iterative_deepening":
            result = iterative_deepening(start, end, request.blocks, request.size, request.directions, dx, dy)
        elif request.algorithm == "bidirectional":
            result = bidirectional_search(start, end, request.blocks, request.size, request.directions, dx, dy)
        elif request.algorithm == "local_beam":
            result = local_beam_search(start, end, request.blocks, request.size, request.directions, dx, dy, request.beam_width)
        elif request.algorithm == "rrt":
            result = rrt(start, end, request.blocks, request.size, request.directions, dx, dy)
        elif request.algorithm == "greedy_best_first":
            result = greedy_best_first(start, end, request.blocks, request.size, request.directions, dx, dy, request.heuristic_type)
        
        if result["path"] is None:
            return SolveResponse(
                path=None, 
                exploration_order=result["exploration_order"],
                error="No path found",
                metrics=result["metrics"]
            )
        
        return SolveResponse(
            path=[[p.first, p.second] for p in result["path"]],
            exploration_order=result["exploration_order"],
            metrics=result["metrics"]
        )
    except Exception as e:
        return SolveResponse(
            path=None,
            exploration_order=[],
            error=str(e),
            metrics={
                "explored_size": 0,
                "frontier_size": 0,
                "time_taken_ms": 0,
                "path_length": 0
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 