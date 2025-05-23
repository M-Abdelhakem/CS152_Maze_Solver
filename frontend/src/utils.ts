import { DELAY, VISITED_CELL_COLOR } from "./constants"

export class Pair {
  constructor(public first: number, public second: number) {}
}

export function make2dArray<T>(size: number, fill: T): T[][] {
  const result: T[][] = []
  for (let i = 0; i < size; i++) result.push(new Array<T>(size).fill(fill))
  return result
}

export async function sleep(time = DELAY) {
  await new Promise((r) => setTimeout(r, time))
}

export function setCellColor(i: number, j: number, color = VISITED_CELL_COLOR) {
  document.getElementById(`c-${i}-${j}`)!.style.animation = `cellVisited 0.5s forwards`
  document.getElementById(`c-${i}-${j}`)!.style.backgroundColor = color
} 