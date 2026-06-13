from problem import Problem
from nsga2 import NSGA2
from population import Population
from common_operators import CommonOperators

class MOmTSP:
    def __init__(self, 
            problem : Problem,
            population_size : int,
            mutation_probability : float,
            iterations : int
    ):
        self.problem = problem        
        self.mutation_probability = mutation_probability
        self.population = Population(iterations, population_size)

    def start_problem(self):
        self.population.create_initial_population(self.problem)
        ranks = NSGA2.fast_non_dominated_sort(self.population.actual_population)
        for rank in ranks:
            NSGA2.crowding_distance(rank)
        return ranks

    def solve(self):
        ranks = self.start_problem()
        NSGA2.print_ranks(ranks)
        iteration_counter = 0

        population_for_crossover = CommonOperators.binary_tournament_selection(self.population.actual_population)
        print(population_for_crossover)

        # while iteration_counter < self.population.generations:
