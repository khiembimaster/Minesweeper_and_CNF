def solve_cnf(clauses, assigned, n, m):
    used_variables = {abs(i) for clause in clauses for i in clause}

    def backtrack(variable_index, assignment):
        if variable_index == len(used_variables):
            if check(assignment, assigned):
                return all(eval_clause(clause, assignment) for clause in clauses)
            else:
                return False
        temp=list(used_variables)
        variable = temp[variable_index]

        assignment[variable] = True
        if backtrack(variable_index + 1, assignment):
            return True

        assignment[variable] = False
        if backtrack(variable_index + 1, assignment):
            return True

        assignment[variable] = None
        return False

    def find_start(i):
        if (i//10 -1>0):
            if(i%10 -1>0):
                start=(i//10 -1)*10+(i%10-1)
            else:
                start=(i//10 -1)*10+(i%10)
        else:
            if(i%10 -1>0):
                start=(i//10)*10+(i%10-1)
            else:
                start=(i//10)*10+(i%10)
        return start
    
    
    def check(assignment,assigned):
        for i in assigned:
            temp0=assigned[i] 
            sum=0   
            i=int(i)

            start=find_start(i)

            if (i//10 +1<=n):
                if(i%10 +1<=m):
                    end=(i//10 +1)*10+(i%10+1)
                else:
                    end=(i//10 +1)*10+(i%10)
            else:
                if(i%10 +1<=m):
                    end=(i//10)*10+(i%10+1)
                else:
                    end=(i//10)*10+(i%10)

            for j in range(start//10,end//10+1,1):
                for z in range(start%10,(end+1)%10,1):
                    x=j*10+z
                    if f"{x}"not in assigned.keys():
                        temp=assignment[x]
                        if (temp):
                            sum+=1
            if sum!=temp0:
                return False
        return True
    
    assignment = {var: None for var in used_variables}
    if backtrack(0, assignment):
        return assignment
    return None

def eval_clause(clause, assignment):
    for i in clause:
        variable = abs(i)
        value = assignment[variable]
        if i > 0:
            if value:
                return True
        else:
            if not value:
                return True
    return False

def finish(solution):
    if solution:
        result=[]
    for var, value in solution.items():
        variable_name = f"{var}"
        if value:
            result.append(int(variable_name))
    for i in result:
        print(i)
