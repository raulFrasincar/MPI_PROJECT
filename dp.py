import time
import tracemalloc
import random
from collections import Counter

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

def resolve(c1, c2, var):
    return (c1 - {var}) | (c2 - {-var})

def eliminate_variable(clauses, var):
    pos = {c for c in clauses if var in c}
    neg = {c for c in clauses if -var in c}
    rest = {c for c in clauses if var not in c and -var not in c}

    resolvents = set()
    for c1 in pos:
        for c2 in neg:
            resolvent = resolve(c1, c2, var)
            if any(-lit in resolvent for lit in resolvent):
                continue
            resolvents.add(frozenset(resolvent))

    return rest.union(resolvents)

def choose_variable_order(clauses, strategy='first'):
    symbols = [abs(lit) for clause in clauses for lit in clause]
    symbol_counts = Counter(symbols)
    unique_symbols = list(symbol_counts.keys())

    if strategy == 'first':
        return unique_symbols
    elif strategy == 'random':
        random.shuffle(unique_symbols)
        return unique_symbols
    elif strategy == 'most_frequent':
        return [var for var, _ in symbol_counts.most_common()]
    elif strategy == 'least_frequent':
        return [var for var, _ in symbol_counts.most_common()][::-1]
    else:
        raise ValueError("Unknown strategy")

def dp_solver(clauses, strategy='first'):
    symbols = choose_variable_order(clauses, strategy)

    for var in symbols:
        clauses = eliminate_variable(clauses, var)
        if frozenset() in clauses:
            return False

    return True

if __name__ == "__main__":
    dimacs = """
    p cnf 3 3
    1 2 0
    -1 3 0
    -2 -3 0
    """

    strategy = "most_frequent"  # first, random, most_frequent, least_frequent

    clauses = parse_dimacs(dimacs)

    tracemalloc.start()
    start = time.perf_counter()
    result = dp_solver(clauses, strategy=strategy)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Strategy: {strategy}")
    print("Result:", "SAT" if result else "UNSAT")
    print("Time:", "{:.5f} seconds".format(end - start))
    print("Memory:", round(peak / 1024, 2), "KB")
