import {
  DEFAULT_SIZE,
  MAX_SIZE,
  PATH_COLOR,
  TARGET_LOCATION_COLOR,
  VISITED_CELL_COLOR,
  WEIGHT_COLORS,
} from "./constants"
import {
  Pair,
  sleep,
  make2dArray,
  setCellColor
} from "./utils"
import "./style.css"
import { solveMaze } from './services/mazeService';

// Add algorithm name mapping at the top of the file after imports
const algorithmNames: { [key: string]: string } = {
  'bfs': 'BFS',
  'dfs': 'DFS',
  'dijkstra': "Dijkstra",
  'astar': 'A*',
  'iterative_deepening': 'IDDFS',
  'bidirectional': 'Bidirectional',
  'local_beam': 'Local Beam',
  'rrt': 'RRT',
  'greedy_best_first': 'Greedy Best-First',
  'ucs': 'UCS'
};

let grid = document.getElementById("grid"),
  select = document.getElementById("mode"),
  algorithmSelectBox = document.getElementById("algorithm"),
  startBtn = document.getElementById("start")

let mode: "blocks" | "target" | "location" | "weights" = "blocks",
  algorithm: "bfs" | "dfs" | "dijkstra" | "astar" | "iterative_deepening" | "bidirectional" | "local_beam" | "rrt" | "greedy_best_first" | "ucs" = "bfs"

function main(size = DEFAULT_SIZE) {
  const blocks = make2dArray(size, false)
  const weights = make2dArray(size, 1)
  let isWeighted = false
  let isSolved = false

  grid!.style.gridTemplateColumns = `repeat(${size}, 1fr)`
  // Add fixed dimensions to the grid to prevent resizing
  grid!.style.width = '100%'
  grid!.style.height = 'auto'
  grid!.style.aspectRatio = '1 / 1'
  grid!.style.maxWidth = '800px'
  grid!.style.maxHeight = '800px'

  let target = new Pair(size - 1, size - 1),
    location = new Pair(0, 0)

  // Create metrics display element
  const metricsDisplay = document.createElement('div');
  metricsDisplay.id = 'metrics-display';
  metricsDisplay.className = 'mt-8 p-4 bg-white border border-gray-300 rounded-lg shadow-md hidden w-full';
  metricsDisplay.innerHTML = `
    <div class="max-w-4xl mx-auto">
      <h3 class="text-xl font-bold mb-2">Algorithm Performance Metrics</h3>
      
      <div class="mb-4 p-3 bg-blue-50 rounded-lg">
        <h4 class="font-semibold text-blue-800">Algorithm Complexity</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2">
          <div>
            <p class="font-medium text-blue-700">Time Complexity:</p>
            <p id="time-complexity" class="text-sm">O(n) where n is the number of cells</p>
            <p class="text-xs text-gray-500">Theoretical worst-case time to find a path</p>
          </div>
          <div>
            <p class="font-medium text-blue-700">Space Complexity:</p>
            <p id="space-complexity" class="text-sm">O(n) where n is the number of cells</p>
            <p class="text-xs text-gray-500">Maximum memory required during execution</p>
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-gray-50 p-3 rounded-lg">
          <p class="font-semibold text-gray-700">Explored Cells</p>
          <p class="text-2xl font-bold text-blue-600"><span id="explored-size">0</span></p>
          <p class="text-xs text-gray-500">Total unique cells visited during search</p>
        </div>
        <div class="bg-gray-50 p-3 rounded-lg">
          <p class="font-semibold text-gray-700">Frontier Size</p>
          <p class="text-2xl font-bold text-green-600"><span id="frontier-size">0</span></p>
          <p class="text-xs text-gray-500">Cells waiting to be explored at end of search</p>
        </div>
        <div class="bg-gray-50 p-3 rounded-lg">
          <p class="font-semibold text-gray-700">Time Taken</p>
          <p class="text-2xl font-bold text-purple-600"><span id="time-taken">0</span> ms</p>
          <p class="text-xs text-gray-500">Actual execution time in milliseconds</p>
        </div>
        <div class="bg-gray-50 p-3 rounded-lg">
          <p class="font-semibold text-gray-700">Path Length</p>
          <p class="text-2xl font-bold text-red-600"><span id="path-length">0</span></p>
          <p class="text-xs text-gray-500">Number of steps in the found path</p>
        </div>
      </div>
      <div class="mt-3 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-gray-50 p-3 rounded-lg">
          <p class="font-semibold text-gray-700">Total Cost</p>
          <p class="text-2xl font-bold text-orange-600"><span id="total-cost">0</span></p>
          <p class="text-xs text-gray-500">Sum of weights along the path</p>
        </div>
        <div class="bg-gray-50 p-3 rounded-lg">
          <p class="font-semibold text-gray-700">Exploration Efficiency</p>
          <p class="text-2xl font-bold text-indigo-600"><span id="exploration-efficiency">0</span></p>
          <p class="text-xs text-gray-500">Ratio of explored cells to path length (lower is better)</p>
        </div>
        <div class="bg-gray-50 p-3 rounded-lg">
          <p class="font-semibold text-gray-700">Memory Usage</p>
          <p class="text-2xl font-bold text-amber-600"><span id="memory-usage">0</span></p>
          <p class="text-xs text-gray-500">Total cells stored (frontier + explored)</p>
        </div>
        <div class="bg-gray-50 p-3 rounded-lg">
          <p class="font-semibold text-gray-700">Time Efficiency</p>
          <p class="text-2xl font-bold text-teal-600"><span id="time-efficiency">0</span></p>
          <p class="text-xs text-gray-500">Milliseconds per path step (lower is better)</p>
        </div>
      </div>
      <div class="mt-3 text-xs text-gray-500 italic">
        <p>Note: Lower values for Exploration Efficiency and Time Efficiency indicate better performance.</p>
      </div>
    </div>
  `;
  
  // Create a container for the maze and options
  const mazeContainer = document.createElement('div');
  mazeContainer.className = 'flex flex-col md:flex-row gap-4 mb-8';
  mazeContainer.style.minHeight = '800px'; // Increase minimum height to match the larger grid
  
  // Move the grid and options into the container
  const optionsContainer = document.getElementById('options')!;
  mazeContainer.appendChild(optionsContainer);
  mazeContainer.appendChild(grid!);
  
  // Clear the app container and add the new structure
  const appContainer = document.getElementById('app')!;
  appContainer.innerHTML = '';
  appContainer.appendChild(mazeContainer);
  appContainer.appendChild(metricsDisplay);

  // Add weighted maze toggle button to options container
  const weightedToggle = document.createElement('div');
  weightedToggle.className = 'mb-4';
  weightedToggle.innerHTML = `
    <label class="flex items-center space-x-2">
      <input type="checkbox" id="weighted-toggle" class="form-checkbox h-5 w-5 text-blue-600">
      <span>Enable Weighted Maze</span>
    </label>
  `;
  // Insert after the title (h1 element)
  const titleElement = optionsContainer.querySelector('h1');
  if (titleElement) {
    optionsContainer.insertBefore(weightedToggle, titleElement.nextSibling);
  } else {
    optionsContainer.insertBefore(weightedToggle, optionsContainer.firstChild);
  }

  // Add weight controls
  const weightControls = document.createElement('div');
  weightControls.id = 'weight-controls';
  weightControls.className = 'mb-4 hidden';
  weightControls.innerHTML = `
    <div class="flex items-center space-x-4">
      <button id="random-weights" class="px-3 py-2 bg-blue-500 text-white rounded-md">
        Random Weights
      </button>
      <div class="flex items-center space-x-2">
        <label>Weight:</label>
        <input type="number" id="weight-value" min="1" max="9" value="1" 
          class="w-16 px-2 py-1 border rounded">
      </div>
    </div>
  `;
  // Insert after the weighted toggle
  optionsContainer.insertBefore(weightControls, weightedToggle.nextSibling);

  // Add weighted maze event listeners
  const weightedToggleCheckbox = document.getElementById('weighted-toggle') as HTMLInputElement;
  const weightControlsDiv = document.getElementById('weight-controls')!;
  const randomWeightsBtn = document.getElementById('random-weights')!;
  const weightValueInput = document.getElementById('weight-value') as HTMLInputElement;

  weightedToggleCheckbox.addEventListener('change', () => {
    isWeighted = weightedToggleCheckbox.checked;
    weightControlsDiv.classList.toggle('hidden', !isWeighted);
    if (!isWeighted) {
      // Reset weights to 1 when disabling weighted mode
      weights.forEach(row => row.fill(1));
      render();
    }
  });

  randomWeightsBtn.addEventListener('click', () => {
    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        if (!blocks[i][j]) {
          weights[i][j] = Math.floor(Math.random() * 9) + 1;
        }
      }
    }
    render();
  });

  function render() {
    grid!.innerHTML = ""
    grid!.style.gridTemplateColumns = `repeat(${size}, 1fr)`
    // Set CSS variable for grid size
    grid!.style.setProperty('--size', size.toString())
    
    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        const isLocation = location.first === i && location.second === j
        const isTarget = target.first === i && target.second === j
        const weight = weights[i][j]
        const weightColor = isWeighted && !blocks[i][j] ? WEIGHT_COLORS[weight - 1] : ''

        grid!.innerHTML += `
          <button id="c-${i}-${j}" i="${i}" j="${j}" class="cell ${
          blocks[i][j] ? "blocked" : ""
        }" style="background: ${
          isLocation || isTarget ? TARGET_LOCATION_COLOR : weightColor
        }">
            ${isLocation ? "A" : isTarget ? "B" : isWeighted && !blocks[i][j] ? weight : ""}
          </button>
        `
      }
    }
    
    let isMouseDown = false

    document.addEventListener("mousedown", () => {
      isMouseDown = true
    })

    document.addEventListener("mouseup", () => {
      isMouseDown = false
    })

    document.querySelectorAll(".cell").forEach((cell) => {
      cell.addEventListener("click", () => {
        if (isSolved) {
          render()
          isSolved = false
        }

        const i = +cell.getAttribute("i")!,
          j = +cell.getAttribute("j")!

        if (mode === "blocks") {
          if ((location.first !== i || location.second !== j) &&
              (target.first !== i || target.second !== j)) {
            blocks[i][j] = !blocks[i][j]
            if (blocks[i][j]) {
              document.getElementById(`c-${i}-${j}`)!.classList.add("blocked")
              weights[i][j] = 1  // Reset weight when blocking
            } else {
              document.getElementById(`c-${i}-${j}`)!.classList.remove("blocked")
            }
          }
        } else if (mode === "weights" && isWeighted) {
          if (!blocks[i][j] && 
              (location.first !== i || location.second !== j) &&
              (target.first !== i || target.second !== j)) {
            const newWeight = +weightValueInput.value
            weights[i][j] = newWeight
            document.getElementById(`c-${i}-${j}`)!.style.backgroundColor = WEIGHT_COLORS[newWeight - 1]
            document.getElementById(`c-${i}-${j}`)!.innerText = newWeight.toString()
          }
        }

        // preventing collision with target and location positions
        if (
          mode === "location" &&
          !blocks[i][j] &&
          (target.first !== i || target.second !== j)
        ) {
          document.getElementById(
            `c-${location.first}-${location.second}`
          )!.style.backgroundColor = "white"
          document.getElementById(
            `c-${location.first}-${location.second}`
          )!.innerText = ""
          location.first = i
          location.second = j
          document.getElementById(
            `c-${location.first}-${location.second}`
          )!.style.backgroundColor = TARGET_LOCATION_COLOR
          document.getElementById(
            `c-${location.first}-${location.second}`
          )!.innerText = "A"
        }

        // preventing collision with blocks and target positions
        if (
          mode === "target" &&
          !blocks[i][j] &&
          (location.first !== i || location.second !== j)
        ) {
          document.getElementById(
            `c-${target.first}-${target.second}`
          )!.style.backgroundColor = "white"
          document.getElementById(
            `c-${target.first}-${target.second}`
          )!.innerText = ""
          target.first = i
          target.second = j
          document.getElementById(
            `c-${target.first}-${target.second}`
          )!.style.backgroundColor = TARGET_LOCATION_COLOR
          document.getElementById(
            `c-${target.first}-${target.second}`
          )!.innerText = "B"
        }
      })
      cell.addEventListener("mouseover", () => {
        if (!isMouseDown) return
        if (isSolved) {
          render()
          isSolved = false
        }

        const i = +cell.getAttribute("i")!,
          j = +cell.getAttribute("j")!

        if (
          mode === "blocks" &&
          (location.first !== i || location.second !== j) &&
          (target.first !== i || target.second !== j)
        ) {
          blocks[i][j] = !blocks[i][j]
          if (blocks[i][j])
            document.getElementById(`c-${i}-${j}`)!.classList.add("blocked")
          else
            document.getElementById(`c-${i}-${j}`)!.classList.remove("blocked")
        }
      })
      cell.addEventListener("mousedown", () => {
        if (isSolved) {
          render()
          isSolved = false
        }

        const i = +cell.getAttribute("i")!,
          j = +cell.getAttribute("j")!

        if (
          mode === "blocks" &&
          (location.first !== i || location.second !== j) &&
          (target.first !== i || target.second !== j)
        ) {
          blocks[i][j] = !blocks[i][j]
          if (blocks[i][j])
            document.getElementById(`c-${i}-${j}`)!.classList.add("blocked")
          else
            document.getElementById(`c-${i}-${j}`)!.classList.remove("blocked")
        }
      })
      cell.addEventListener("mouseup", () => {
        if (isSolved) {
          render()
          isSolved = false
        }

        const i = +cell.getAttribute("i")!,
          j = +cell.getAttribute("j")!

        if (
          mode === "blocks" &&
          (location.first !== i || location.second !== j) &&
          (target.first !== i || target.second !== j)
        ) {
          blocks[i][j] = !blocks[i][j]
          if (blocks[i][j])
            document.getElementById(`c-${i}-${j}`)!.classList.add("blocked")
          else
            document.getElementById(`c-${i}-${j}`)!.classList.remove("blocked")
        }
      })
    })
  }

  select!.addEventListener("change", () => {
    mode = (<HTMLSelectElement>document.getElementById("mode")).value as
      | "blocks"
      | "target"
      | "location"
      | "weights"
  })

  algorithmSelectBox!.addEventListener("change", () => {
    algorithm = (<HTMLSelectElement>algorithmSelectBox).value as
      | "bfs"
      | "dfs"
      | "dijkstra"
      | "astar"
      | "greedy_best_first"
      | "iterative_deepening"
      | "bidirectional"
      | "local_beam"
      | "rrt"
      | "ucs"

    // show the a* options and remove them if not selected
    if (algorithm === "astar" || algorithm === "greedy_best_first") {
      document.querySelector("#heuristic")!.classList.remove("hidden")
      document.querySelector("#heuristic-label")!.classList.remove("hidden")
    } else {
      document.querySelector("#heuristic")!.classList.add("hidden")
      document.querySelector("#heuristic-label")!.classList.add("hidden")
    }
    
    // show the beam width input and update max value if local beam is selected
    if (algorithm === "local_beam") {
      document.querySelector("#beam-width")!.classList.remove("hidden")
      document.querySelector("#beam-width-label")!.classList.remove("hidden")
      
      // Set max value to size - 1 (number of cells per row minus 1)
      const sizeInput = document.getElementById("size") as HTMLInputElement
      const beamWidthInput = document.getElementById("beam-width") as HTMLInputElement
      beamWidthInput.max = (parseInt(sizeInput.value) - 1).toString()
      
      // Add input event listener to validate beam width as user types
      beamWidthInput.addEventListener("input", () => {
        const maxBeamWidth = parseInt(beamWidthInput.max)
        const currentValue = parseInt(beamWidthInput.value)
        
        if (currentValue > maxBeamWidth) {
          beamWidthInput.setCustomValidity(`Value must be less than or equal to ${maxBeamWidth}`)
        } else {
          beamWidthInput.setCustomValidity("")
        }
      })
    } else {
      document.querySelector("#beam-width")!.classList.add("hidden")
      document.querySelector("#beam-width-label")!.classList.add("hidden")
    }
    
    // Force a re-render to ensure the grid layout is correct
    render()
  })

  startBtn?.addEventListener("click", async () => {
    isSolved = true
    render()

    const directions = +(<HTMLSelectElement>(
      document.getElementById("directions")
    )).value

    const algorithm = (<HTMLSelectElement>algorithmSelectBox).value
    const heuristicType = +(<HTMLSelectElement>document.getElementById("heuristic")).value
    const beamWidthInput = document.getElementById("beam-width") as HTMLInputElement
    const beamWidth = +beamWidthInput.value
    
    // Validate beam width if local beam algorithm is selected
    if (algorithm === "local_beam") {
      const maxBeamWidth = parseInt(beamWidthInput.max)
      if (beamWidth > maxBeamWidth) {
        // Show error message
        beamWidthInput.setCustomValidity(`Value must be less than or equal to ${maxBeamWidth}`)
        beamWidthInput.reportValidity()
        return
      } else {
        // Clear any previous error
        beamWidthInput.setCustomValidity("")
      }
    }

    const request = {
      start: [location.first, location.second] as [number, number],
      end: [target.first, target.second] as [number, number],
      blocks: blocks,
      weights: isWeighted ? weights : undefined,
      size: size,
      directions: directions,
      algorithm: algorithm,
      heuristic_type: heuristicType,
      beam_width: beamWidth,
      is_weighted: isWeighted
    };

    const response = await solveMaze(request);
    
    if (response.error) {
      console.error('Error:', response.error);
      showAlert(`No solution found! Couldn't find a path from (A) to (B) with the ${algorithmNames[algorithm]} in this maze configuration.`);
      return;
    }

    // First, visualize the exploration process
    for (const [x, y] of response.exploration_order) {
      if (x !== location.first || y !== location.second) {
        if (x !== target.first || y !== target.second) {
          await sleep(10);
          document.getElementById(`c-${x}-${y}`)!.style.backgroundColor = VISITED_CELL_COLOR;
        }
      }
    }

    // Then, visualize the final path
    if (response.path) {
      for (const [x, y] of response.path) {
        if (x !== location.first || y !== location.second) {
          if (x !== target.first || y !== target.second) {
            await sleep(10);
            document.getElementById(`c-${x}-${y}`)!.style.backgroundColor = PATH_COLOR;
          }
        }
      }
    } else {
      // No path found - display an animated alert
      showAlert(`No solution found! Couldn't find a path from start (A) to end (B) with the ${algorithm} algorithm in this maze configuration.`);
    }
    
    // Display metrics
    document.getElementById('metrics-display')!.classList.remove('hidden');
    
    // Ensure all metrics are properly initialized
    const metrics = {
      explored_size: response.metrics.explored_size || 0,
      frontier_size: response.metrics.frontier_size || 0,
      time_taken_ms: response.metrics.time_taken_ms || 0,
      path_length: response.metrics.path_length || 0,
      total_cost: response.metrics.total_cost || 0
    };
    
    // Update basic metrics
    document.getElementById('explored-size')!.textContent = metrics.explored_size.toString();
    document.getElementById('frontier-size')!.textContent = metrics.frontier_size.toString();
    document.getElementById('time-taken')!.textContent = metrics.time_taken_ms.toFixed(2);
    document.getElementById('path-length')!.textContent = metrics.path_length.toString();
    document.getElementById('total-cost')!.textContent = metrics.total_cost.toString();
    
    // Calculate additional metrics with proper error handling
    const explorationEfficiency = metrics.path_length > 0 
      ? (metrics.explored_size / metrics.path_length).toFixed(2) 
      : '0';
    document.getElementById('exploration-efficiency')!.textContent = explorationEfficiency;
    
    const memoryUsage = metrics.explored_size + metrics.frontier_size;
    document.getElementById('memory-usage')!.textContent = memoryUsage.toString();
    
    const timeEfficiency = metrics.path_length > 0 
      ? (metrics.time_taken_ms / metrics.path_length).toFixed(2) 
      : '0';
    document.getElementById('time-efficiency')!.textContent = timeEfficiency;
    
    // Set algorithm complexity information with detailed explanations
    let timeComplexity = '';
    let spaceComplexity = '';
    
    switch(algorithm) {
      case 'bfs':
        timeComplexity = 'O(n) where n is the number of cells';
        spaceComplexity = 'O(n) where n is the number of cells';
        break;
      case 'dfs':
        timeComplexity = 'O(n) where n is the number of cells';
        spaceComplexity = 'O(h) where h is the maximum depth of the recursion';
        break;
      case 'dijkstra':
        timeComplexity = 'O(n log n) where n is the number of cells';
        spaceComplexity = 'O(n) where n is the number of cells';
        break;
      case 'astar':
        timeComplexity = 'O(n log n) where n is the number of cells';
        spaceComplexity = 'O(n) where n is the number of cells';
        break;
      case 'iterative_deepening':
        timeComplexity = 'O(b^d) where b is branching factor and d is depth';
        spaceComplexity = 'O(d) where d is the depth of the solution';
        break;
      case 'bidirectional':
        timeComplexity = 'O(n) where n is the number of cells';
        spaceComplexity = 'O(n) where n is the number of cells';
        break;
      case 'local_beam':
        timeComplexity = 'O(b * w * d) where b is beam width, w is width of maze, d is depth';
        spaceComplexity = 'O(b * w) where b is beam width, w is width of maze';
        break;
      case 'rrt':
        timeComplexity = 'O(n log n) where n is the number of nodes in the tree';
        spaceComplexity = 'O(n) where n is the number of nodes in the tree';
        break;
      case 'greedy_best_first':
        timeComplexity = 'O(n log n) where n is the number of cells';
        spaceComplexity = 'O(n) where n is the number of cells';
        break;
      case 'ucs':
        timeComplexity = 'O(b^d) where b is branching factor and d is depth';
        spaceComplexity = 'O(b) where b is branching factor';
        break;
    }
    
    document.getElementById('time-complexity')!.textContent = timeComplexity;
    document.getElementById('space-complexity')!.textContent = spaceComplexity;
    
    // Add tooltips with explanations
    const tooltips = {
      'exploration-efficiency': 'Lower values indicate better exploration efficiency (fewer cells explored per path length)',
      'time-efficiency': 'Lower values indicate better time efficiency (less time taken per path length)',
      'memory-usage': 'Total number of cells stored in memory during the search',
      'explored-size': 'Number of cells visited during the search',
      'frontier-size': 'Number of cells waiting to be explored',
      'time-taken': 'Time taken to find the path in milliseconds',
      'path-length': 'Length of the found path'
    };
    
    // Add tooltips to each metric
    Object.entries(tooltips).forEach(([id, tooltip]) => {
      const element = document.getElementById(id);
      if (element) {
        element.title = tooltip;
      }
    });
    
    // Scroll to metrics
    metricsDisplay.scrollIntoView({ behavior: 'smooth' });
  })

  render()
}

main(DEFAULT_SIZE)

function syncSizeForm() {
  const input = <HTMLInputElement>document.getElementById("size")
  input.value = DEFAULT_SIZE.toString()
  input.max = MAX_SIZE.toString()

  // Update beam width max value when size changes
  input.addEventListener("input", () => {
    const beamWidthInput = document.getElementById("beam-width") as HTMLInputElement
    if (beamWidthInput) {
      beamWidthInput.max = (parseInt(input.value) - 1).toString()
    }
  })

  document.getElementById("form")?.addEventListener("submit", (e) => {
    e.preventDefault()
    const sizeInput = (<HTMLInputElement>document.getElementById("size")).value

    // recreate the button to remove event listeners
    let newBtn = startBtn!.cloneNode(true)
    startBtn!.parentNode!.replaceChild(newBtn, startBtn!)
    startBtn = newBtn as HTMLElement

    main(+sizeInput)
  })
}

syncSizeForm()

// Function to show an animated alert
function showAlert(message: string) {
  // Get the alert container from the HTML
  const alertContainer = document.getElementById('alert-container');
  if (!alertContainer) {
    console.error('Alert container not found');
    return;
  }
  
  // Create alert element
  const alert = document.createElement('div');
  alert.className = 'alert';
  alert.textContent = message;
  
  // Add alert to container
  alertContainer.appendChild(alert);
  
  // Remove alert after 5 seconds
  setTimeout(() => {
    alert.classList.add('hiding');
    setTimeout(() => {
      alert.remove();
    }, 500); // Match the animation duration
  }, 5000);
}

// Add this at the beginning of the file, after the imports
document.addEventListener('DOMContentLoaded', () => {
  // Initialize alert container if it doesn't exist
  if (!document.getElementById('alert-container')) {
    const alertContainer = document.createElement('div');
    alertContainer.id = 'alert-container';
    alertContainer.className = 'alert-container';
    document.body.appendChild(alertContainer);
  }
});
