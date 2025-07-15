from satinstance import SATInstance 
import random
import os

def print_assignment(assignment):
    for i, bool in enumerate(assignment):
        if bool == None: continue
        print(f"Literal {i+1} set to {bool}")

def randomize_assignment(assignment):
    #random number of literals assigned
    for i in range(random.randint(0, len(assignment)-1)):
        literal = random.randint(0, len(assignment)-1)
        while assignment[literal] != None:
            literal = random.randint(0, len(assignment)-1)
        assignment[literal] = random.choice([True, False])
    return assignment

#check testing w/ random assignments
# with open(f"tests/uf20-91/{random.choice(os.listdir("tests/uf20-91"))}", "r") as file:
#     instance = SATInstance.instance_from_file(SATInstance, file)
#     print(instance)
#     print()

#     z = instance.assignment.copy()
#     randomize_assignment(z)
#     print_assignment(z)

#     print(f"check result: {instance.check(z)}")
#     print()

#     print(instance)

#two sat testing
with open(f"tests/uf20-91/{random.choice(os.listdir("tests/uf20-91"))}", "r") as file:
    instance = SATInstance.instance_from_file(SATInstance, file)
    print(instance)
    print()

    z = instance.assignment.copy()
    randomize_assignment(z)
    print_assignment(z)

    print(f"check result: {instance.check(z)}")
    print()

    print(instance)