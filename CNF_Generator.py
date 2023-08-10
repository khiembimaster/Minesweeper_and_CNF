import numpy as np
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Solver
import Bruteforce
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
            assigned[f'{i+1}{j+1}'] = int(board[i][j])
        else:
            unassigned.add(f'{i+1}{j+1}')

def unassign_neighbors(x, unassigned, n, m):
    s = []
    i = int(x[0])-1
    j = int(x[1])-1
    for k in range(i-1,i+2):
        if k < 0 or k >= n:
            continue
        for l in range(j-1,j+2):
            if l < 0 or l >= m:
                continue
            if k==i and l==j:
                continue
            if f'{k+1}{l+1}' in unassigned:
                s.append(f'{k+1}{l+1}')
    return s

for a,i in assigned.items():
    neighbors = unassign_neighbors(a,unassigned, n,m) 
    pos = combinations(neighbors,len(neighbors)-i+1)
    neg = combinations(neighbors,i+1)
    for clause in pos:
        clauses.append([int(liter) for liter in clause])
    for clause in neg:
        clauses.append([-int(liter) for liter in clause])


print(assigned)
print(unassigned)
print(clauses)
for a in unassigned:
    satisfy = True
    ### A*
    clauses.append([int(a)])
    problem = Astar.Problem(clauses)
    satisfy = not Astar.AStar(problem)

    ### BACK-TRACK

    ### BRUTE-FORCE
    # satisfy = not (Bruteforce.resolution(clauses))
    ## PYSAT
    # clauses.append([-int(a)])
    # cnf = CNF(from_clauses=clauses)
    # with Solver(bootstrap_with=cnf) as solver:
    #     satisfy = solver.solve()
    #     print(solver.get_model())
    
    clauses.pop(-1)

    if not satisfy:
        print(a)
        board[int(a[0])-1][int(a[1])-1] = 'X'
        clauses.append([int(a)])

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