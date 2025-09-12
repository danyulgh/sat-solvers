class Pigeonhole:
    def generate(n, m): #n pigeons, m holes
        clauses = []
        for i in range(1, n+1):
            clause = [f"{i}{j}" for j in range(1, m+1)] #pigeon i can go into hole j
            clauses.append(clause)
        
        for i in range(1, m+1): # for every hole i
            for j in range(1, n + 1): # each pigeon j...
                for k in range(j+1, n+1): # and each pigeon k in front of j...
                    clause = [f"-{j}{i}", f"-{k}{i}"] # then j and k cannot both be in hole i
                    clauses.append(clause)

        num_vars = n*m
        num_clauses = len(clauses)

        with open(f"generated/{n}-pigeons_{m}-holes.cnf", "w") as f:
            f.write(f"c generated pigeonhole with {n} pigeons and {m} holes \n")
            f.write(f"p cnf {num_vars} {num_clauses} \n")
            for clause in clauses:
                f.write(" ".join(map(str, clause)) + " 0\n")
        
        print(f"CNF written to generated/{n}-pigeons_{m}-holes.cnf")