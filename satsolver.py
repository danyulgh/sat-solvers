from satinstance import SATInstance 
import time 
import os
import csv

heuristics = [SATInstance.frequent, SATInstance.moms, SATInstance.jeroslow_wang]
test_dirs = [2, 3, 4]

for test_dir in test_dirs: # for each category of tests
    for heuristic in heuristics: # cycle thru heuristics
        with open(f"results/minus/{test_dir}/{heuristic.__name__}.csv", "w", newline='') as f: # creates the csv file
            writer = csv.writer(f)
            writer.writerow(["n", "time", "variables", "clauses"])
            f.close()
        for test in os.listdir(f"generated/minus/{test_dir}"): # cycle thru test in the category
            with open(f"generated/minus/{test_dir}/{test}", "r") as f: # open the test file
                instance = SATInstance.instance_from_file(SATInstance, f)
                print(f"test: {test}, heuristic: {heuristic.__name__}, clauses: {len(instance.clauses)}, variables: {len(instance.variables)}")
                f.close()
            assignment = [None] * len(instance.variables)
            start_time = time.perf_counter()
            instance.solve(assignment, heuristic)
            end_time = time.perf_counter()
            with open(f"results/minus/{test_dir}/{heuristic.__name__}.csv", "a", newline='') as f: # adds to the csv file
                writer = csv.writer(f)
                writer.writerow([int(test[:2]), end_time-start_time, len(instance.variables), len(instance.clauses)])
                f.close()
            if end_time - start_time > 100: # stop testing heursitic with the category if longer than 10 minutes
                break