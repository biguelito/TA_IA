from solver import Solver

import timeit
import random

if __name__ == "__main__":
    random.seed(42)
    
    solver = Solver()
    solution = solver.solve_eil51()

    