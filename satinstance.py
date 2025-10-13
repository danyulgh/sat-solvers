from collections import defaultdict
from collections import Counter

class SATInstance:
    def __init__(self):
        self.variables = [] #list of variables
        self.variable_table = dict() #assignment of variable to position in variables
        self.clauses = []
    
    def instance_from_file(cls, file):
        #construct instance
        instance = cls()
        for line in file: # parse lines
            line = line.strip()
            if line.startswith("c"): continue #skip comments 
            if line.startswith("p"): continue
            if line.startswith("%"): break
            instance.add_clause(line)
        return instance
    
    def add_clause(self, line):
        clause = []
        for literal in line.split():
            if literal == "0": break #0 is the end of a clause
            clause.append(int(literal)) #add literal to clause
            variable = abs(int(literal)) #get abs of literal as a variable
            if variable not in self.variable_table: #add variable to table
                self.variable_table[variable] = len(self.variables)
                self.variables.append(variable)
        self.clauses.append(tuple(clause)) #the clause is immutable

    def check(self, assignment):
        #updating clauses based on assignment 
        new_clauses = []
        for i, clause in enumerate(self.clauses):
            new_clause = self.check_clause(clause, assignment) #update clause with assignment            
            if new_clause == True: continue #clause is true, so don't add it to new clauses
            elif new_clause == False: return False #clause is false so unsat
            new_clauses.append(tuple(new_clause)) #clause was not simplified so add it back
        self.clauses = new_clauses
        #if no new clauses left, then were satisfied
        if len(new_clauses) == 0: return True
        return None
        
    def check_clause(self, clause, assignment):
        #expression defaults to false
        expression = False
        new_clause = []
        for literal in clause:
            assignment_key = self.variable_table[abs(literal)]
            #if there is no assignment for the literal, add it to the new clause
            if assignment[assignment_key] == None:
                new_clause.append(literal)
                continue
            #expression or (if literal is assigned to true)
            expression = expression or not assignment[assignment_key] if literal < 0 else assignment[assignment_key]
            #clause is true if any literal is true
            if expression: return True
        #if there is no new_clause and expression is False, then the clause is false
        if not expression and not new_clause: return False
        #if there is a new clause, return it
        return new_clause
    
    def is_twosat(self):
        #checks if we can run 2 sat
        for clause in self.clauses:
            if len(clause) > 2: return False
        return True

    def twosat(self):
        #running 2 sat
        graph = sat_graph()
        for clause in self.clauses:
            graph.add_clause(clause)
        if graph.has_contradiction(): return False
        self.clauses = []
        return True

    def find_pures(self):
        pures = set()
        not_pures = set()
        #for each literal in the clauses
        for clause in self.clauses:
            for literal in clause:
                #if the -literal is in pures, remove it from pures
                #and add the literal to not pures so it can never be added to pures again
                if -literal in pures:
                    pures.remove(-literal)
                    not_pures.add(abs(literal))
                #if the abs literal is not in not pures, then add the literal to pures
                elif abs(literal) not in not_pures:
                    pures.add(literal)
        return pures

    def find_units(self):
        #finds every unit value
        units = []
        for clause in self.clauses:
            if len(clause) == 1: units.append(clause[0])
        return units
    
    def stand(self, assignment):
        #run 2 sat if <=2 literals every clause
        if self.is_twosat(): return self.twosat()
        #assign pure literals so they're true
        for pure in self.find_pures(): assignment[self.variable_table[abs(pure)]] = False if pure < 0 else True
        #assign unit clauses to be true
        for unit in self.find_units(): assignment[self.variable_table[abs(unit)]] = False if unit < 0 else True 
        temp_clauses = self.clauses.copy()
        check = self.check(assignment)
        #check had a true or false, meaning there was a sat or unsat
        if check != None: return check
        #clauses were simplified, run stand again
        if self.clauses != temp_clauses: return self.stand(assignment)
        #no simplification happened, return None
        return None

    def frequent(self):
        counter = Counter()
        for clause in self.clauses:
            for literal in clause:
                counter[abs(literal)] += 1
        return counter.most_common()[0][0]
    
    def least_frequent(self):
        counter = Counter()
        for clause in self.clauses:
            for literal in clause:
                counter[abs(literal)] += 1
        return counter.most_common()[-1][0]

    def spread(self):
        counter = Counter()
        for clause in self.clauses:
            found = [False] * len(self.variables)
            for literal in clause:
                assignment_key = self.variable_table[abs(literal)]
                if found[assignment_key]: continue
                counter[abs(literal)] += 1
                found[assignment_key] = True
        return counter.most_common()[0][0]

    def moms(self):
        min_size = min([len(clause) for clause in self.clauses])
        counter = Counter()
        for clause in self.clauses:
            if len(clause) == min_size:
                for literal in clause:
                    counter[abs(literal)] += 1
        return counter.most_common()[0][0]
    
    def jeroslow_wang(self):
        counter = Counter()
        for clause in self.clauses:
            for literal in clause:
                counter[abs(literal)] += 2 ** (-len(clause))
        return counter.most_common()[0][0]
    
    def solve(self, assignment, var_func):
        if (stand := self.stand(assignment)) != None: return stand
        var = var_func(self)
        for value in [True, False]:
            assignment_key = self.variable_table[var]
            new_assignment = assignment.copy()
            new_assignment[assignment_key] = value
            temp_clauses = self.clauses.copy()
            if self.solve(new_assignment, var_func): return True
            self.clauses = temp_clauses
        return False

class sat_graph:
    def __init__(self):
        self.graph = defaultdict(set)
        self.nodes = set()
    
    def __str__(self):
        edges = ""
        for node in self.graph:
            for neighbor in self.graph[node]:
                edges += f"({node}, {neighbor})\n"
        return edges
        
    def addEdge(self, u, v):
        self.graph[u].add(v)
        self.nodes.add(u)
        self.nodes.add(v)
    
    def add_clause(self, clause):
        if len(clause) == 2:
            self.addEdge(-clause[0], clause[1])
            self.addEdge(-clause[1], clause[0])
        else:
            self.addEdge(-clause[0], clause[0])
    
    def has_contradiction(self):
        for component in self.strongly_connected_components():
            literals = set()
            for literal in component:
                if -literal in literals: return True
                literals.add(literal)
        return False

    def DFS(self, visited, stack, scc):
        for node in self.nodes:
            if node not in visited:
                self.traverse(visited, node, stack, scc)

    def traverse(self, visited, node, stack, scc):
        if node not in visited:
            visited.append(node)
            for neighbor in self.graph[node]:
                self.traverse(visited, neighbor, stack, scc)
            stack.append(node)
            scc.append(node)
        return visited

    def strongly_connected_components(self):
        stack = []
        sccs = []
        self.DFS([], stack, [])
        transposed = self.transpose_graph()
        visited = []
        while stack:
            node = stack.pop()
            if node not in visited:
                scc = []
                scc.append(node)
                transposed.traverse(visited, node, [], scc)
                sccs.append(scc)
        return sccs

    def transpose_graph(self):
        transposed = sat_graph()
        for node in self.graph:
            for neighbor in self.graph[node]:
                transposed.addEdge(neighbor, node)
        return transposed