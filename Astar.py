from dataclasses import dataclass, field
import heapq
import sys
import bisect

class Problem():
    def __init__(self, INIT):
        self._INITIAL_STATE = tuple(i for i in range(INIT))

    def GOAL_TEST(self, STATE):
        n = len(STATE)
        for i in range(n-1):
            for j in range(i+1, n):
                if (STATE[i] == STATE [j]) or (abs(STATE[i]-STATE[j]) == abs(i-j)):
                    return False
        return True

    def ACTIONS(self, STATE:list):
        n = len(STATE)
        childSets = []
        for i in range(n):
            for j in range(1, n):
                temp = STATE.copy()
                temp[i] = (STATE[i] + j) % n
                childSets.append(tuple(temp))
        return childSets

@dataclass(frozen=True, order=True)
class AStarNode():
    state:tuple=field(compare=False, hash=True)
    cost:float=field(compare=False)
    estimated_total_cost:float

def heuristic(state:tuple):
    estimated_forward_cost = 0
    n = len(state)
    for i in range(n-1):
        for j in range(i+1, n):
            if (state[i] == state[j]) or (abs(state[i]-state[j]) == abs(i-j)):
                estimated_forward_cost += 1
    return estimated_forward_cost

def AStar(problem:Problem):
    node = AStarNode(problem._INITIAL_STATE, 0, heuristic(problem._INITIAL_STATE))
    frontier = [node]
    explored = set([])

    while frontier.count != 0:
        node = heapq.heappop(frontier)
        print(node)
        if problem.GOAL_TEST(node.state):
            return (node)
        explored.add(node)
        actions = problem.ACTIONS(list(node.state))
        for action in actions:
            child = AStarNode(action, 1 + node.cost, 1 + node.cost + heuristic(action))
            in_frontier = bisect.bisect_left(frontier, child)
            if in_frontier < len(frontier) and child.state == frontier[in_frontier].state:
                if child < frontier[in_frontier]:
                    frontier[in_frontier] = child
            elif child not in explored:
                heapq.heappush(frontier, child)
    return None