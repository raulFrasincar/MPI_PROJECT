import itertools
import time
import tracemalloc

def parse_dimacs(dimacs):
    lines = dimacs.strip().split('\n')
    clauses = set()

    for line in lines:
        line = line.strip()
        if line.startswith('c') or line.startswith('p'):
            continue
        literals = list(map(int, line.split()))
        literals = [lit for lit in literals if lit != 0]
        clause = frozenset(literals)

        if any(-lit in clause for lit in clause):
            continue

        clauses.add(clause)

    return clauses

def resolve(c1, c2):
    for lit in c1:
        if -lit in c2:
            resolvent = (c1.union(c2)) - {lit, -lit}
            if any(-l in resolvent for l in resolvent):
                return None
            return frozenset(resolvent)
    return None

def resolution_solver(clauses, max_iter=100):
    new = set()
    all_clauses = set(clauses)

    for _ in range(max_iter):
        pairs = list(itertools.combinations(all_clauses, 2))
        for (ci, cj) in pairs:
            resolvent = resolve(ci, cj)
            if resolvent is None:
                continue
            if len(resolvent) == 0:
                return False
            new.add(resolvent)

        if new.issubset(all_clauses):
            return True

        all_clauses.update(new)

    return True

if __name__ == "__main__":
    dimacs = """
    p cnf 3 3
    1 2 0
    -1 3 0
    -2 -3 0
    """

    clauses = parse_dimacs(dimacs)

    tracemalloc.start()
    start = time.time()
    result = resolution_solver(clauses)
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("Result:", "SAT" if result else "UNSAT")
    print("Time:", "{:.5f} seconds".format(end - start))
    print("Memory:", round(peak / 1024, 2), "KB")
