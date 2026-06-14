from problem import Problem
from momtsp import MOmTSP

import timeit
import random

mutation_probability = 0.05
population_size = 100

def do_eil51():
    salesman_quantity = 7    
    problem = Problem("eil51", salesman_quantity)
    iterations = 1400

    pareto_front = MOmTSP(problem,
                    population_size=population_size, 
                    mutation_probability=mutation_probability,
                    iterations=iterations).solve()
    
    last = pareto_front[-1]
    semilast = pareto_front[-2]

    print(pareto_front)
    print(last.chromossome)
    print(semilast.chromossome)

def time_eil51():
    salesman_quantity = 7    
    problem = Problem("eil51", salesman_quantity)
    iterations = 1400

    momtsp = MOmTSP(problem,
                    population_size=population_size, 
                    mutation_probability=mutation_probability,
                    iterations=iterations)
    
    exec_time = timeit.timeit(lambda:momtsp.solve(), number=10)
    print(exec_time)

if __name__ == "__main__":
    # random.seed(42)
    
    time_eil51()