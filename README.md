# Pac-Man Search Algorithms | Group 51

![Python 3](https://img.shields.io/badge/Python-3-3776AB)

An Intelligent Agents university group assignment based on the UC Berkeley Pac-Man Search project. Group 51 implements graph search algorithms, a corner-visiting problem representation, and heuristics that guide Pac-Man through mazes and food-collection tasks.

The required assignment covers **Q1–Q7**, with a verified score of **22/22**. Q8 is part of the original starter project, is outside this assignment's requirements, and remains unimplemented.

> **Distribution restriction:** The original source notice prohibits distributing or publishing solutions. A public repository containing these implementations conflicts with that restriction unless separate permission is obtained. See [Attribution and distribution restrictions](#attribution-and-distribution-restrictions) before publishing.

## Project objectives

- Implement DFS, BFS, UCS, and A* as reusable graph search algorithms.
- Represent navigation and multi-goal tasks through states, successors, goal tests, and action costs.
- Develop admissible, consistent heuristics for visiting all corners and collecting all food.
- Compare solution costs and expanded search nodes using the supplied layouts and autograder.

## Implemented algorithms and problems

### Search algorithms

The implementations in [search.py](search.py) return a sequence of actions for a supplied search problem.

| Question | Algorithm | Function / alias | Search strategy |
| --- | --- | --- | --- |
| Q1 | Depth First Search (DFS) | `depthFirstSearch` / `dfs` | Uses a stack to explore deeper states first; does not guarantee a shortest path. |
| Q2 | Breadth First Search (BFS) | `breadthFirstSearch` / `bfs` | Uses a queue to explore by depth; finds a shortest path by number of actions. |
| Q3 | Uniform Cost Search (UCS) | `uniformCostSearch` / `ucs` | Uses a priority queue ordered by accumulated path cost, `g(n)`. |
| Q4 | A* Search | `aStarSearch` / `astar` | Uses a priority queue ordered by `g(n) + h(n)`, tracking cheaper paths and allowing states to be reopened. |

UCS finds a minimum-cost path for nonnegative step costs. A* uses a heuristic lower bound to guide that search; the examples below use Manhattan distance or the assignment's problem-specific heuristics.

### Problem representations and heuristics

These classes and functions are in [searchAgents.py](searchAgents.py).

| Component | State or approach | Purpose |
| --- | --- | --- |
| `PositionSearchProblem` (provided) | Pac-Man position `(x, y)` | Reach a specified goal position; used by the Q1–Q4 maze examples. |
| `CornersProblem` (Q5) | `(position, visited_corners)`, with visited corners stored as a `frozenset` | Visit all four corners using unit-cost moves. |
| `cornersHeuristic` (Q6) | Minimum sum of Manhattan distances across every ordering of the unvisited corners | Estimate the remaining cost without accounting for walls; used by `AStarCornersAgent`. |
| `FoodSearchProblem` (provided) | `(position, foodGrid)` | Collect every remaining food dot using unit-cost moves. |
| `foodHeuristic` (Q7) | Manhattan distance to the nearest food plus the weight of a minimum spanning tree over the remaining food, also using Manhattan distances | Estimate the remaining collection cost; used by `AStarFoodSearchAgent`. |

## Technologies and dependencies

- **Python 3** and its standard library. The commands below were verified with Python **3.14.3**.
- **Tkinter / Tcl/Tk** for the graphical display. A desktop display is needed to open the game window; `-q` runs Pac-Man without graphics.
- **Bundled Berkeley framework and autograder** for game logic, layouts, search utilities, and evaluation.

No third-party Python packages are required. This repository has no `requirements.txt` or Python package installation step. Git is optional if the repository is downloaded as a ZIP archive.

## Project structure

```text
IA-Pacman-Search-Group51/
├── README.md              # Project documentation
├── search.py              # DFS, BFS, UCS, and A* implementations
├── searchAgents.py        # Search agents, problem definitions, and heuristics
├── pacman.py              # Game entry point and command-line options
├── game.py                # Core game state and rules infrastructure
├── util.py                # Stacks, queues, priority queues, and helpers
├── layout.py              # Layout loading
├── layouts/               # Maze definitions (*.lay)
├── graphicsDisplay.py     # Graphical Pac-Man display
├── graphicsUtils.py       # Tkinter graphics helpers
├── textDisplay.py         # Text and non-graphical displays
├── keyboardAgents.py      # Keyboard-controlled agent
├── pacmanAgents.py        # Additional provided Pac-Man agents
├── ghostAgents.py         # Provided ghost agents
├── eightpuzzle.py          # Additional provided search problem
├── autograder.py           # Autograder entry point
├── grading.py             # Grading and reporting utilities
├── projectParams.py       # Autograder project configuration
├── searchTestClasses.py    # Search-specific test definitions
├── testClasses.py          # Shared test infrastructure
├── testParser.py           # Test-file parser
├── test_cases/             # Tests, reference solutions, and configuration
│   ├── CONFIG
│   ├── q1/ … q7/          # Required assignment questions
│   └── q8/                # Original starter tests; outside assignment scope
├── VERSION                # Starter project version information
└── .gitignore
```

## Installation and setup

1. Install Python 3. Include Tcl/Tk support if you want to use the graphical display.
2. Obtain an authorized copy of this repository through your course's approved sharing method, then open a terminal in its root directory—the folder containing `pacman.py` and `autograder.py`.
3. Check the interpreter and available command-line options:

   ```sh
   python --version
   python pacman.py --help
   python autograder.py --help
   ```

The examples use `python`. If your Python 3 interpreter is invoked as `python3` or `py`, substitute that command throughout.

## Running Pac-Man

Run these commands from the repository root. Each example uses a layout and agent included in this repository. The `-q` option selects a quiet, non-graphical run; remove it for the graphical display or replace it with `-t` for text animation.

### Q1: Depth First Search

```sh
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs -q
```

### Q2: Breadth First Search

```sh
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs -q
```

### Q3: Uniform Cost Search

```sh
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs -q
```

This example uses the default unit-cost `PositionSearchProblem`. The supplied UCS autograder also exercises varying step costs.

### Q4: A* with Manhattan distance

```sh
python pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic -q
```

### Q5: CornersProblem with BFS

```sh
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem -q
```

### Q6: A* with the corners heuristic

```sh
python pacman.py -l mediumCorners -p AStarCornersAgent -q
```

`AStarCornersAgent` selects `CornersProblem` and `cornersHeuristic`. The verified run expands **741 nodes**.

### Q7: FoodSearchProblem with A*

```sh
python pacman.py -l trickySearch -p AStarFoodSearchAgent -q
```

`AStarFoodSearchAgent` selects `FoodSearchProblem` and `foodHeuristic`. The verified run expands **7,137 nodes**.

## Autograder and results

Run the required questions individually to keep evaluation within the assignment scope:

```sh
python autograder.py -q q1 --no-graphics
python autograder.py -q q2 --no-graphics
python autograder.py -q q3 --no-graphics
python autograder.py -q q4 --no-graphics
python autograder.py -q q5 --no-graphics
python autograder.py -q q6 --no-graphics
python autograder.py -q q7 --no-graphics
```

The autograder also runs prerequisite questions where configured: Q5 includes Q2, and Q6/Q7 include Q4. Count each question once when calculating the required assignment total.

| Question | Component | Verified score | Expanded nodes on the indicated benchmark |
| --- | --- | ---: | --- |
| Q1 | DFS | 3/3 | — |
| Q2 | BFS | 3/3 | — |
| Q3 | UCS | 3/3 | — |
| Q4 | A* | 3/3 | — |
| Q5 | CornersProblem | 3/3 | — |
| Q6 | Corners heuristic | 3/3 | 741 (`mediumCorners`) |
| Q7 | Food heuristic | 4/4 | 7,137 (`trickySearch`) |
| **Required total** | **Q1–Q7** | **22/22** | |

The scores and node counts above were reproduced using the included autograder. Dashes indicate that no single benchmark count is reported for that question; they do not mean zero expansions.

**Q7 output note:** The `food_heuristic_grade_tricky` test prints `FAIL` because 7,137 expansions exceed its strictest threshold of 7,000. Its scoring logic still awards one base point plus three threshold points, producing **Q7: 4/4**. This result does not claim that every performance threshold was met.

**Q8 scope:** Running `python autograder.py --no-graphics` without `-q` includes the original Q8 tests. Q8 is unimplemented and excluded from the required **22/22** total; the full starter-suite total should not be presented as the assignment score.

On Python 3.14.3, the supplied `grading.py` may emit an invalid-escape `SyntaxWarning`; it did not prevent the documented runs from completing. Autograder scores are local results—follow the course's submission process to receive official credit.

## Team contributions

Replace these placeholders with the four members' details and their actual contributions before submission.

| Member | Name | Student ID | Contributions |
| --- | --- | --- | --- |
| 1 | [Member 1 name] | [Student ID] | [Implemented questions, testing, review, or documentation] |
| 2 | [Member 2 name] | [Student ID] | [Implemented questions, testing, review, or documentation] |
| 3 | [Member 3 name] | [Student ID] | [Implemented questions, testing, review, or documentation] |
| 4 | [Member 4 name] | [Student ID] | [Implemented questions, testing, review, or documentation] |

## Attribution and distribution restrictions

This assignment builds on the original **UC Berkeley Pac-Man AI project**. The core projects and autograders were primarily created by **John DeNero** and **Dan Klein**. Student-side autograding was added by **Brad Miller**, **Nick Hay**, and **Pieter Abbeel**. Group 51's work covers the Q1–Q7 implementations described above; the underlying framework and supplied problems retain their original attribution.

Original attribution link: [http://ai.berkeley.edu](http://ai.berkeley.edu).

The licensing and attribution notice below is retained from [search.py](search.py). The original notices in the source files must also be retained.

```text
Licensing Information: You are free to use or extend these projects for
educational purposes provided that (1) you do not distribute or publish
solutions, (2) you retain this notice, and (3) you provide clear
attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

Attribution Information: The Pacman AI projects were developed at UC Berkeley.
The core projects and autograders were primarily created by John DeNero
(denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
Student side autograding was added by Brad Miller, Nick Hay, and
Pieter Abbeel (pabbeel@cs.berkeley.edu).
```

**Conflict with a public-repository requirement:** Publishing this repository's completed solutions would conflict with the quoted restriction. If the course requires a public GitHub repository, raise this conflict with the instructor and seek an approved submission arrangement or separate permission from the rights holder before publication. Keep solution access restricted to the course-authorized submission workflow in the meantime. Attribution alone does not remove the restriction.
