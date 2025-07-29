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

directories = ["tests/uf20-91", "tests/uf50-218", "tests/uuf50-218/UUF50.218.1000"]
picking = [SATInstance.most_frequent, SATInstance.most_spread]
for i in range(30):
    directory = random.choice(directories)
    pick = random.choice(picking)
    with open(f"{directory}/{random.choice(os.listdir(directory))}", "r") as file:
        instance = SATInstance.instance_from_file(SATInstance, file)
        assignment = [None] * instance.count
        start_time = time.perf_counter()
        value = instance.solve(assignment, pick)
        end_time = time.perf_counter()
        print(f"{file.name}: {end_time-start_time} seconds for {"SAT" if value else "UNSAT"} via {pick.__name__}")