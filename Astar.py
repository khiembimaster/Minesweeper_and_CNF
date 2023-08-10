from dataclasses import dataclass, field
from itertools import combinations
import heapq
import sys
import bisect

@dataclass(frozen=True, order=True)
class AStarNode():
    model:dict=field(compare=False, hash=False)
    _hash:frozenset=field(hash=True)
    cost:float=field(compare=False)
    estimated_total_cost:float

class Problem():
    def __init__(self, KB):
        self.KB = KB[:-1]
        self.a = [KB[-1]]
        self.symbols = {}
        self.frequency = {}
        for clause in KB:
            for symbol in clause:
                c_symbol = str(symbol) 
                if c_symbol not in self.frequency:
                    self.frequency[c_symbol] = 1
                else:
                    self.frequency[c_symbol] += 1
                self.symbols[str(abs(symbol))]=0

    def PL_TRUE(self, model:dict, clauses = None):
        if clauses == None:
            clauses = self.KB
        for clause in clauses:
            sum = 0
            for symbol in clause:
                if (symbol > 0) == model[str(abs(symbol))]:
                    sum+=1
                    break
            if sum == 0:
                return False
        return True

    def PL_TRUE_heuristic(self, model:dict):
        h = 0
        for key, value in model.items():
            k = key if value == 1 else f'-{key}'
            if k in self.frequency:
                h += self.frequency[k]
        return h

    def ACTIONS(self, model:dict):
        childSets = []
        for key,value in model.items():
            temp = model.copy()
            temp[key] = (value+1)%2
            childSets.append(temp)
        return childSets

def AStar(problem:Problem):
    node = AStarNode(problem.symbols, frozenset(problem.symbols.items()), 0, 0)
    frontier = [node]
    explored = set([])

    while len(frontier) > 0:
        node = heapq.heappop(frontier)
        # print(node)
        if problem.PL_TRUE(node.model):
            return problem.PL_TRUE(node.model, problem.a)
        
        explored.add(node)
        actions = problem.ACTIONS(node.model)
        for action in actions:
            # + problem.PL_TRUE_heuristic(action)
            child = AStarNode(action,frozenset(action.items()), -1 - node.cost, -1 -node.cost - problem.PL_TRUE_heuristic(action))
            in_frontier = bisect.bisect_left(frontier, child)
            if in_frontier < len(frontier) and child.model == frontier[in_frontier].model:
                if child < frontier[in_frontier]:
                    frontier[in_frontier] = child
            elif child not in explored:
                heapq.heappush(frontier, child)
    return None

# def TT_Entails(KB,)