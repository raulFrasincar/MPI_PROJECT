import time
import tracemalloc
from collections import Counter
from random import choice, shuffle

def parse_dimacs_string(dimacs_str):
    clauses = []
    for line in dimacs_str.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("c") or line.startswith("p"):
            continue
        tokens = line.split()
        if tokens[-1] != "0":
            continue
        clause = set(tokens[:-1])
        clauses.append(frozenset(clause))
    return clauses

def choose_literal(clauses, assignment, strategy="first"):
    all_lits = [lit for clause in clauses for lit in clause]
    unassigned = [lit for lit in all_lits if lit.lstrip("-") not in assignment]
    if not unassigned:
        return None
    if strategy == "first":
        return unassigned[0]
    elif strategy == "most_frequent":
        counts = Counter(unassigned)
        return counts.most_common(1)[0][0]
    elif strategy == "random":
        return choice(unassigned)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

def unit_propagate(clauses, assignment):
    changed = True
    while changed:
        changed = False
        unit_clauses = [c for c in clauses if len(c) == 1]
        for unit in unit_clauses:
            lit = next(iter(unit))
            val = not lit.startswith("-")
            var = lit.lstrip("-")
            if var in assignment:
                continue
            assignment[var] = val
            clauses = simplify(clauses, lit)
            changed = True
    return clauses, assignment

def simplify(clauses, lit):
    new_clauses = []
    comp = "-" + lit if not lit.startswith("-") else lit[1:]
    for clause in clauses:
        if lit in clause:
            continue
        if comp in clause:
            clause = set(clause)
            clause.remove(comp)
            new_clauses.append(frozenset(clause))
        else:
            new_clauses.append(clause)
    return new_clauses

def dpll_solver(clauses, assignment={}, strategy="first"):
    clauses, assignment = unit_propagate(clauses, assignment)
    if not clauses:
        return True
    if frozenset() in clauses:
        return False

    lit = choose_literal(clauses, assignment, strategy)
    if lit is None:
        return True

    var = lit.lstrip("-")
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = val
        test_lit = var if val else "-" + var
        new_clauses = simplify(clauses, test_lit)
        if dpll_solver(new_clauses, new_assignment, strategy):
            return True
    return False

def main():
    dimacs = """
    p cnf 3 3
    1 2 0
    -1 3 0
    -2 -3 0
    """

    strategy = "first"  # first, most_frequent, random
    clauses = parse_dimacs_string(dimacs)

    print(f"Parsed {len(clauses)} clauses.")
    print(f"Branching strategy: {strategy}")

    tracemalloc.start()
    start = time.time()
    result = dpll_solver(clauses, {}, strategy)
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\nDPLL result:", "SAT" if result else "UNSAT")
    print("Time:", "{:.5f} seconds".format(end - start))
    print("Memory peak:", round(peak / 1024, 2), "KB")

if __name__ == "__main__":
    main()
