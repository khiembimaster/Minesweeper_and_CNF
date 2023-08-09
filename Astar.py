from dataclasses import dataclass, field
from itertools import combinations
import heapq
import sys
import bisect

class Problem():
    def __init__(self, INIT):
        self._INITIAL_STATE = INIT

    def GOAL_TEST(self, STATE):
        if STATE in self._INITIAL_STATE:
            return False
        return True

    def ACTIONS(self, STATE:list):
        return [[Ci, Cj] for Ci, Cj in combinations(STATE,2)]

@dataclass(frozen=True, order=True)
class AStarNode():
    state:list=field(compare=False, hash=True)
    cost:int=field(compare=False)
    estimated_total_cost:int

def heuristic(state):
    return len(state)

def resolve(Ci:list,Cj:list):

    count = 0
    resolvents = None
    for i in range(len(Ci)):
        for j in range(len(Cj)):
            if Ci[i]+Cj[j] == 0:
                if count == 1:
                    return None
                _Ci = Ci.copy()
                _Cj = Cj.copy()
                _Ci.pop(i)
                _Cj.pop(j)     
                count+=1           
                resolvents = tuple(set(_Ci+_Cj)) 
    
    return resolvents

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
        actions = problem.ACTIONS(node.state)
        for Ci, Cj in actions:
            child = AStarNode(action, 1 + node.cost, 1 + node.cost + heuristic(action))
            in_frontier = bisect.bisect_left(frontier, child)
            if in_frontier < len(frontier) and child.state == frontier[in_frontier].state:
                if child < frontier[in_frontier]:
                    frontier[in_frontier] = child
            elif child not in explored:
                heapq.heappush(frontier, child)
    return None

# p = Problem([])
# actions = p.ACTIONS([[11,12], [13], [14]])
# print(actions)
