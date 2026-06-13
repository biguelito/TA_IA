from problem import Problem
from nsga2 import NSGA2
from population import Population

class MOmTSP:
    def __init__(self, 
            problem : Problem,
            population_size : int,
            mutation_probability : float,
            iterations : int
    ):
        self.problem = problem        
        self.mutation_probability = mutation_probability
        # self.nsga2 = NSGA2()
        self.population = Population(iterations, population_size)

    def start_problem(self):
        self.population.create_initial_population(self.problem)
        # nsga2 = NSGA2()
        ranks = NSGA2.fast_non_dominated_sort(self.population.actual_population)
        for rank in ranks:
            NSGA2.crowding_distance(rank)
        return ranks

    def solve(self):
        ranks = self.start_problem()
        NSGA2.print_ranks(ranks)
        