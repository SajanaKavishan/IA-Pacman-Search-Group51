
# searchAgents.py
# ---------------
# Licensing Information: You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeal@cs.berkeley.edu).

"""
This file contains all of the agents that can be selected to control Pacman.
"""

from typing import List, Tuple, Any
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import pacman


class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP


#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow
    that path.

    Note: You should NOT change any code in SearchAgent.
    """

    def __init__(
        self,
        fn='depthFirstSearch',
        prob='PositionSearchProblem',
        heuristic='nullHeuristic'
    ):
        if fn not in dir(search):
            raise AttributeError(
                fn + ' is not a search function in search.py.'
            )

        func = getattr(search, fn)

        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(
                    heuristic +
                    ' is not a function in searchAgents.py or search.py.'
                )

            print(
                '[SearchAgent] using function %s and heuristic %s'
                % (fn, heuristic)
            )

            self.searchFunction = lambda x: func(
                x, heuristic=heur
            )

        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(
                prob + ' is not a search problem type in SearchAgents.py.'
            )

        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        if self.searchFunction is None:
            raise Exception("No search function provided for SearchAgent")

        starttime = time.time()
        problem = self.searchType(state)
        self.actions = self.searchFunction(problem)

        if self.actions is None:
            self.actions = []

        totalCost = problem.getCostOfActions(self.actions)

        print(
            'Path found with total cost of %d in %.1f seconds'
            % (totalCost, time.time() - starttime)
        )

        if '_expanded' in dir(problem):
            print(
                'Search nodes expanded: %d'
                % problem._expanded
            )

    def getAction(self, state):
        if 'actionIndex' not in dir(self):
            self.actionIndex = 0

        i = self.actionIndex
        self.actionIndex += 1

        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class PositionSearchProblem(search.SearchProblem):
    """
    A search problem whose states are Pacman positions.
    """

    def __init__(
        self,
        gameState,
        costFn=lambda x: 1,
        goal=(1, 1),
        start=None,
        warn=True,
        visualize=True
    ):
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()

        if start is not None:
            self.startState = start

        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize

        if warn and (
            gameState.getNumFood() != 1
            or not gameState.hasFood(*goal)
        ):
            print('Warning: this does not look like a regular search maze')

        self._visited = {}
        self._visitedlist = []
        self._expanded = 0  # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__

            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):
                    __main__._display.drawExpandedCells(
                        self._visitedlist
                    )

        return isGoal

    def getSuccessors(self, state):
        successors = []

        for action in [
            Directions.NORTH,
            Directions.SOUTH,
            Directions.EAST,
            Directions.WEST
        ]:
            x, y = state
            dx, dy = Actions.directionToVector(action)

            nextx = int(x + dx)
            nexty = int(y + dy)

            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)

                successors.append(
                    (nextState, action, cost)
                )

        self._expanded += 1  # DO NOT CHANGE

        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        if actions is None:
            return 999999

        x, y = self.getStartState()
        cost = 0

        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x = int(x + dx)
            y = int(y + dy)

            if self.walls[x][y]:
                return 999999

            cost += self.costFn((x, y))

        return cost


class StayEastSearchAgent(SearchAgent):
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(
            state, costFn, (1, 1), None, False
        )


class StayWestSearchAgent(SearchAgent):
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(
            state, costFn
        )


def manhattanHeuristic(position, problem, info={}):
    xy1 = position
    xy2 = problem.goal

    return (
        abs(xy1[0] - xy2[0])
        + abs(xy1[1] - xy2[1])
    )


def euclideanHeuristic(position, problem, info={}):
    xy1 = position
    xy2 = problem.goal

    return (
        (xy1[0] - xy2[0]) ** 2
        + (xy1[1] - xy2[1]) ** 2
    ) ** 0.5


#####################################################
# Q5 – CORNERS PROBLEM (MEMBER 1)
#####################################################

class CornersProblem(search.SearchProblem):
    """
    Find a path that visits all four corners of the maze.

    State:
        (current_position, visited_corners)
    """

    def __init__(self, startingGameState: pacman.GameState):
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()

        top = self.walls.height - 2
        right = self.walls.width - 2

        self.corners = (
            (1, 1),
            (1, top),
            (right, 1),
            (right, top)
        )

        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print(
                    'Warning: no food in corner ' + str(corner)
                )

        self._expanded = 0  # DO NOT CHANGE

    def getStartState(self):
        if self.startingPosition in self.corners:
            visited = frozenset([self.startingPosition])
        else:
            visited = frozenset()

        return (self.startingPosition, visited)

    def isGoalState(self, state):
        position, visited_corners = state

        return len(visited_corners) == len(self.corners)

    def getSuccessors(self, state: Any):
        successors = []

        current_position, visited_corners = state
        x, y = current_position

        for action in [
            Directions.NORTH,
            Directions.SOUTH,
            Directions.EAST,
            Directions.WEST
        ]:
            dx, dy = Actions.directionToVector(action)

            nextx = int(x + dx)
            nexty = int(y + dy)

            if not self.walls[nextx][nexty]:
                next_position = (nextx, nexty)

                if next_position in self.corners:
                    next_visited = (
                        visited_corners
                        | frozenset([next_position])
                    )
                else:
                    next_visited = visited_corners

                next_state = (
                    next_position,
                    next_visited
                )

                successors.append(
                    (next_state, action, 1)
                )

        self._expanded += 1  # DO NOT CHANGE

        return successors

    def getCostOfActions(self, actions):
        if actions is None:
            return 999999

        x, y = self.startingPosition

        for action in actions:
            dx, dy = Actions.directionToVector(action)

            x = int(x + dx)
            y = int(y + dy)

            if self.walls[x][y]:
                return 999999

        return len(actions)


#####################################################
# Q6 – CORNERS HEURISTIC (MEMBER 2)
#####################################################

def cornersHeuristic(state: Any, problem: CornersProblem):
    """
    Estimate the minimum remaining distance needed to
    visit all unvisited corners.

    Uses Manhattan distance and checks every possible
    ordering of the remaining corners.

    This heuristic is admissible and consistent.
    """

    from itertools import permutations

    # Separate current position and visited corners.
    position, visited_corners = state

    # Identify corners that have not been visited.
    remaining_corners = [
        corner
        for corner in problem.corners
        if corner not in visited_corners
    ]

    # If all corners are visited, the goal is reached.
    if not remaining_corners:
        return 0

    # Calculate Manhattan distance between two points.
    def manhattan_distance(point1, point2):
        return (
            abs(point1[0] - point2[0])
            + abs(point1[1] - point2[1])
        )

    # Initially, the best distance is infinity.
    best_distance = float("inf")

    # Examine every possible visiting order.
    for corner_order in permutations(remaining_corners):

        total_distance = 0
        current_position = position

        # Calculate the route through the selected order.
        for corner in corner_order:

            total_distance += manhattan_distance(
                current_position,
                corner
            )

            current_position = corner

        # Keep the shortest estimated route.
        best_distance = min(
            best_distance,
            total_distance
        )

    # Return the admissible estimated remaining cost.
    return best_distance


class AStarCornersAgent(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(
            prob, cornersHeuristic
        )

        self.searchType = CornersProblem


#####################################################
# Q7 – FOOD HEURISTIC (MEMBER 3)
#####################################################

class FoodSearchProblem:
    """
    Search state:
        (pacmanPosition, foodGrid)
    """

    def __init__(self, startingGameState: pacman.GameState):
        self.start = (
            startingGameState.getPacmanPosition(),
            startingGameState.getFood()
        )

        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0  # DO NOT CHANGE
        self.heuristicInfo = {}

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        successors = []
        self._expanded += 1  # DO NOT CHANGE

        for direction in [
            Directions.NORTH,
            Directions.SOUTH,
            Directions.EAST,
            Directions.WEST
        ]:
            x, y = state[0]

            dx, dy = Actions.directionToVector(direction)

            nextx = int(x + dx)
            nexty = int(y + dy)

            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False

                successors.append(
                    (
                        ((nextx, nexty), nextFood),
                        direction,
                        1
                    )
                )

        return successors

    def getCostOfActions(self, actions):
        x, y = self.getStartState()[0]
        cost = 0

        for action in actions:
            dx, dy = Actions.directionToVector(action)

            x = int(x + dx)
            y = int(y + dy)

            if self.walls[x][y]:
                return 999999

            cost += 1

        return cost


class AStarFoodSearchAgent(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(
            prob, foodHeuristic
        )

        self.searchType = FoodSearchProblem


def foodHeuristic(
    state: Tuple[Tuple, List[List]],
    problem: FoodSearchProblem
):
    """
    Estimate the cost of collecting all remaining food
    using nearest-food Manhattan distance plus an MST.
    """

    position, foodGrid = state
    food = foodGrid.asList()

    if not food:
        return 0

    # Manhattan distance to nearest food.
    nearest_food = min(
        abs(position[0] - x) + abs(position[1] - y)
        for x, y in food
    )

    # Build a minimum spanning tree over remaining food.
    remaining = set(food)
    start = food[0]
    remaining.remove(start)

    connected = {start}
    mst_cost = 0

    while remaining:
        best_distance = float("inf")
        best_food = None

        for x1, y1 in connected:
            for x2, y2 in remaining:
                distance = (
                    abs(x1 - x2)
                    + abs(y1 - y2)
                )

                if distance < best_distance:
                    best_distance = distance
                    best_food = (x2, y2)

        mst_cost += best_distance
        connected.add(best_food)
        remaining.remove(best_food)

    return nearest_food + mst_cost


#####################################################
# CLOSEST DOT SEARCH AGENT
#####################################################

class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches."

    def registerInitialState(self, state):
        self.actions = []
        currentState = state

        while currentState.getFood().count() > 0:
            nextPathSegment = self.findPathToClosestDot(
                currentState
            )

            self.actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()

                if action not in legal:
                    t = (str(action), str(currentState))

                    raise Exception(
                        'findPathToClosestDot returned an illegal move: '
                        '%s!\n%s' % t
                    )

                currentState = currentState.generateSuccessor(
                    0, action
                )

        self.actionIndex = 0

        print(
            'Path found with cost %d.'
            % len(self.actions)
        )

    def findPathToClosestDot(
        self,
        gameState: pacman.GameState
    ):
        """
        Returns a path to the closest food dot.
        """

        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    Search problem for finding a path to any food.
    """

    def __init__(self, gameState):
        self.food = gameState.getFood()
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1

        self._visited = {}
        self._visitedlist = []
        self._expanded = 0  # DO NOT CHANGE

    def isGoalState(self, state: Tuple[int, int]):
        x, y = state

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def mazeDistance(
    point1: Tuple[int, int],
    point2: Tuple[int, int],
    gameState: pacman.GameState
) -> int:
    """
    Returns the maze distance between any two points.
    """

    x1, y1 = point1
    x2, y2 = point2

    walls = gameState.getWalls()

    assert not walls[x1][y1], (
        'point1 is a wall: ' + str(point1)
    )

    assert not walls[x2][y2], (
        'point2 is a wall: ' + str(point2)
    )

    prob = PositionSearchProblem(
        gameState,
        start=point1,
        goal=point2,
        warn=False,
        visualize=False
    )

    return len(search.bfs(prob))
