from itertools import combinations

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

def resolution(clauses:list):
    clauses = set(tuple(clause) for clause in clauses)

    while(True):
        new = set()
        for Ci, Cj in combinations(clauses,2):
            resolvent = resolve(list(Ci),list(Cj))
            if resolvent is not None:
                if resolvent == ():
                    return True
                new.add(resolvent)
        if new < clauses:
            return False
        clauses.update(new)

print(resolution([[-21,11],[-11,12,21],[-12,11],[-11],[12]]))