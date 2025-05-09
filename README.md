# MPI_PROJECT

Comparing SAT solving algorithms: Resolution, DP and DPLL.

Includes 3 scripts: resolution.py, dp.py and dpll.py. To input formulas into the script, user will have to edit the "dimacs=" variable found in the main function and add a formula in the DIMACS DNF format. The output will be the number of clauses parsed, the satisifability result (SAT/UNSAT) , the time spent (seconds)  and the memory allocated (KB).

In the case of dp.py and dpll.py, the user has the option of changing the order strategy and the output will show the used strategy and the order of variable elimination or branching strategy.

Example of DIMACS: \
dimacs = """ \
    p cnf 3 3 \
    1 2 0 \
    -1 3 0 \
    -2 -3 0 \
    """
