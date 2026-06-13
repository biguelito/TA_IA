from problem import Problem
from momtsp import MOmTSP


if __name__ == "__main__":
    salesman_quantity = 7    
    problem = Problem("eil51", salesman_quantity)

    population_size = 10
    mutation_probability = 0.05
    iterations = 10
    momtsp = MOmTSP(problem,
                    population_size=population_size, 
                    mutation_probability=mutation_probability,
                    iterations=iterations)
    momtsp.solve()