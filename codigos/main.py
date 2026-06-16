from problem import Problem
from momtsp import MOmTSP

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

def solve_problem(instance, population_size, mutation_probability, iterations, salesman_quantity, repetitions):
    problem = Problem(instance, salesman_quantity)

    momtsp = MOmTSP(problem,
                    population_size=population_size, 
                    mutation_probability=mutation_probability,
                    iterations=iterations)
    solutions = momtsp.solve_repetitions(repetitions)
    return solutions

if __name__ == "__main__":
    random.seed(42)
    
    salesman_quantity = 7  
    iterations = 1400
    repetitions = 1
    mutation_probability = 0.05
    population_size = 100
    print(solve_problem("eil51", population_size, mutation_probability, iterations, salesman_quantity, repetitions))