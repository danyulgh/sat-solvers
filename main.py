from satinstance import SATInstance 
import random
import time 
import os

def print_assignment(z):
    for i, bool in enumerate(z):
        if bool == None: continue
        print(f"Literal {i+1} set to {bool}")

def randomize_assignment(assignment):
    for i in range(random.randint(0, len(assignment)-1)):
        literal = random.randint(0, len(assignment)-1)
        while assignment[literal] != None:
            literal = random.randint(1, len(assignment)-1)
        assignment[literal] = random.choice([True, False])
    return assignment

directories = ["uf20-91", "uf50-218", "uuf50-218/UUF50.218.1000", "flat50-115", "pigeon-hole"]
funcs  = [SATInstance.most_frequent, SATInstance.most_spread]
for i in range(30):
    directory = random.choice(directories)
    # directory = "pigeon-hole"
    test = random.choice(os.listdir(f"tests/{directory}"))
    func = random.choice(funcs)
    with open(f"tests/{directory}/{test}", "r") as file:
        print(f"picking via {test} with {func.__name__}")
        instance = SATInstance.instance_from_file(SATInstance, file)
        assignment = [None] * instance.count
        start_time = time.perf_counter()
        value = instance.solve(assignment, func)
        end_time = time.perf_counter()
        print(f"{file.name}: \033[92m {end_time-start_time} \033[0m seconds for \033[91m {"SAT" if value else "UNSAT"} \033[0m via \033[94m {func.__name__} \033[0m")