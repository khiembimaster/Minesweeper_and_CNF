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
        if (i//n -1>=0):
            if((i%m) -1>=0):
                start=(i//n -1)*n+(i%m-1)
            else:
                start=(i//n -1)*n+(i%m)
        else:
            if(i%m -1>0):
                start=(i//n)*n+(i%m-1)
            else:
                start=(i//n)*n+(i%m)
        return start
    
    def find_end(i):
        if (i//n +1<=n):
            if(i%m +1<=m):
                end=(i//n +1)*m+(i%m+1)
            else:
                end=(i//n +1)*m+(i%m)
        else:
            if(i%10 +1<=m):
                end=(i//10)*m+(i%10+1)
            else:
                end=(i//10)*m+(i%10)
        return end


    def check(assignment,assigned):
        for i in assigned:
            temp0=assigned[i] 
            sum=0   
            i=int(i)

            start=i-1
            if(i%m==1):
                start=i

            end=find_end(i)
            if ((start-1)>0):
                for j in range(start-1,start-4,-1):
                    if (j==0):
                        break
                    if f"{j}"not in assigned.keys():
                        temp=assignment[j]
                        if (temp):
                            sum+=1
            for j in range(start,start+3,1):
                if (j//m>i//m or j==i+2):
                    break
                if f"{j}"not in assigned.keys():
                    temp=assignment[j]
                    if (temp):
                        sum+=1
            if((start+4)//n<=n):
                for j in range(start+4,start+7,1):
                    if (j>m*n):
                        break
                    if f"{j}"not in assigned.keys():
                        temp=assignment[j]
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
