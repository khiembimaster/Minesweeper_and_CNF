import numpy as np
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Solver
from time import perf_counter

import Bruteforce
import Backtracking
import Astar

assigned = {}
unassigned = set()
clauses = []
board = np.loadtxt('input.csv', delimiter=",", dtype=str)
n = len(board)
m = len(board[0])

for i in range(n):
    for j in range(m):
        if int(board[i][j]) > 0:
            assigned[f'{i*m + j + 1}'] = int(board[i][j])
        else:
            unassigned.add(f'{i*m + j + 1}')

def unassign_neighbors(x, unassigned, n, m):
    s = []
    int_x = int(x) - 1
    i = int(int_x/m)
    j = int(int_x%m)
    for k in range(i-1,i+2):
        if k < 0 or k >= n:
            continue
        for l in range(j-1,j+2):
            if l < 0 or l >= m:
                continue
            if k==i and l==j:
                continue
            if f'{k*m + l + 1}' in unassigned:
                s.append(f'{k*m + l + 1}')
    return s

for a,i in assigned.items():
    neighbors = unassign_neighbors(a,unassigned, n,m) 
    pos = combinations(neighbors,len(neighbors)-i+1)
    neg = combinations(neighbors,i+1)
    for clause in pos:
        clauses.append([int(liter) for liter in clause])
    for clause in neg:
        clauses.append([-int(liter) for liter in clause])


# print(assigned)
# print(unassigned)
# print(clauses)

print("1. Pysat")
print("2. A*")
print("3. Backtrack")
print("4. Brute-force")
choice = int(input("Enter algorithm="))

start = perf_counter()
for a in unassigned:
    satisfy = True
    
    ## PYSAT
    if(choice == 1):
        clauses.append([-int(a)])
        cnf = CNF(from_clauses=clauses)
        with Solver(bootstrap_with=cnf) as solver:
            satisfy = solver.solve()

    ### A*
    if(choice ==2):
        clauses.append([int(a)])
        problem = Astar.Problem(clauses)
        satisfy = not Astar.AStar(problem)

    ### BACK-TRACK
    if(choice == 3):
        satisfy = Backtracking.solve_cnf(clauses, assigned, n, m)
        Backtracking.finish(satisfy)    

    ### BRUTE-FORCE
    if(choice == 4):
        satisfy = not (Bruteforce.resolution(clauses))
    
    ## Marking
    clauses.pop(-1)
    if not satisfy:
        print(a)
        board[int((int(a)-1)/m)][int((int(a)-1)%m)] = 'X'
        clauses.append([int(a)])
end = perf_counter()
execution_time = (end - start)*1000
print(f'Time: {execution_time}ms')
np.savetxt('output.csv', board, delimiter=',',fmt='%s')

# nC1 -> A|B|C|D|E
# nCn -> A&B&C&D&E
# nCi -> nC(n-i+1)

# 5C1 -> (A∧¬B∧¬C∧¬D∧¬E)∨(¬A∧B∧¬C∧¬D∧¬E)∨(¬A∧¬B∧C∧¬D∧¬E)∨(¬A∧¬B∧¬C∧D∧¬E)∨(¬A∧¬B∧¬C∧¬D∧E)
# |-> 5C5 -> (A ∨ B ∨ C ∨ D ∨ E) 
# AND
# nC(i+1) -> 5C(1+1)
# |-> 5C2 -> (¬B ∨ ¬A) ∧ (¬C ∨ ¬A) 
#          ∧ (¬C ∨ ¬B) ∧ (¬D ∨ ¬A) 
#          ∧ (¬D ∨ ¬B) ∧ (¬D ∨ ¬C) 
#          ∧ (¬E ∨ ¬A) ∧ (¬E ∨ ¬B) 
#          ∧ (¬E ∨ ¬C) ∧ (¬E ∨ ¬D)

# Prenex conjunctive normal form:
# (A ∨ B ∨ C ∨ D ∨ E) ∧ (¬B ∨ ¬A) ∧ (¬C ∨ ¬A) ∧ (¬C ∨ ¬B) ∧ (¬D ∨ ¬A) ∧ (¬D ∨ ¬B) ∧ (¬D ∨ ¬C) ∧ (¬E ∨ ¬A) ∧ (¬E ∨ ¬B) ∧ (¬E ∨ ¬C) ∧ (¬E ∨ ¬D)

