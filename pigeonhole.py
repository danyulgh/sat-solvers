class Pigeonhole:

    def generate_valids(n, k=1): #n holes, k*n pigeons
        holes = n if k == 1 else n+1
        clauses = []
        for i in range(1, k*n+1):
            clause = [f"{i}{j}" for j in range(1, holes)] #pigeon i can go into hole j
            clauses.append(clause)
        return clauses
    
    def generate_invalids(clauses, n, k=1): #n holes, k*n pigeons
        holes = n if k == 1 else n+1
        for i in range(1, holes): # for every hole i
            for j in range(1, k*n + 1): # each pigeon j...
                for l in range(j+1, k*n+1): # and each pigeon l in front of j...
                    clause = [f"-{j}{i}", f"-{l}{i}"] # then j and l cannot both be in hole i
                    clauses.append(clause)


    def generate(n, filename, k=1): #n pigeons, k*n holes (or n-1 holes if k=1)
        clauses = Pigeonhole.generate_valids(n, k)
        Pigeonhole.generate_invalids(clauses, n, k)

        pigeons = n if k == 1 else n*k
        holes = n-1 if k == 1 else n
        num_vars = n*(n-1) if k == 1 else n*n*k
        num_clauses = len(clauses)

        with open(f"generated/{k}/{filename}_{pigeons}-pigeons_{holes}-holes.cnf", "w") as f:
            f.write(f"c generated pigeonhole with {pigeons} pigeons and {holes} holes \n")
            f.write(f"p cnf {num_vars} vars {num_clauses} clauses \n")
            for clause in clauses:
                f.write(f"{" ".join(map(str, clause)) + " 0"}".strip() + "\n")
        
        print(f"created: {pigeons}-pigeons_{holes}-holes.cnf")

for i in range(5, 10):
    if i < 10:
        Pigeonhole.generate(i, f"0{i}")
        Pigeonhole.generate(i, f"0{i}", 2)
        Pigeonhole.generate(i, f"0{i}", 10)
    else:
        Pigeonhole.generate(i, i)
        Pigeonhole.generate(i, i, 2)
        Pigeonhole.generate(i, i, 10)