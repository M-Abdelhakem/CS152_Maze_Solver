import { Pair } from '../helpers/types';

const API_URL = 'https://3be4-3-147-27-202.ngrok-free.app:8000';

export interface SolveRequest {
  start: [number, number];
  end: [number, number];
  blocks: boolean[][];
  size: number;
  directions: number;
  algorithm: string;
  heuristic_type?: number;
}

export interface SolveResponse {
  path: [number, number][] | null;
  exploration_order: [number, number][];
  error: string | null;
  metrics: {
    explored_size: number;
    frontier_size: number;
    time_taken_ms: number;
    path_length: number;
  };
}

export async function solveMaze(request: SolveRequest): Promise<SolveResponse> {
  try {
    const response = await fetch(`${API_URL}/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error solving maze:', error);
    return {
      path: null,
      exploration_order: [],
      error: error instanceof Error ? error.message : 'Unknown error occurred',
      metrics: {
        explored_size: 0,
        frontier_size: 0,
        time_taken_ms: 0,
        path_length: 0,
      },
    };
  }
} 