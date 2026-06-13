from problem import Problem
from momtsp import MOmTSP
import random


if __name__ == "__main__":
    random.seed(42)
    salesman_quantity = 7    
    problem = Problem("eil51", salesman_quantity)

    population_size = 4
    mutation_probability = 0.05
    iterations = 1
    momtsp = MOmTSP(problem,
                    population_size=population_size, 
                    mutation_probability=mutation_probability,
                    iterations=iterations)
    momtsp.solve()