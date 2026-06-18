from solver import Solver

import timeit
import random


# def time_eil51():
#     mutation_probability = 0.05
#     population_size = 100
#     salesman_quantity = 7    
#     problem = Problem("eil51", salesman_quantity)
#     iterations = 1400

#     momtsp = MOmTSP(problem,
#                     population_size=population_size, 
#                     mutation_probability=mutation_probability,
#                     iterations=iterations)
    
#     exec_time = timeit.timeit(lambda:momtsp.solve(), number=1)
#     print(exec_time)

if __name__ == "__main__":
    random.seed(42)
    
    solver = Solver()
    solution = solver.solve_eil51()

    