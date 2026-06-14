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
        self.common_operators = CommonOperators(problem)
        self.nsga2 = NSGA2()

    def __start_problem(self):
        self.population.create_initial_population(self.problem)
        ranks = self.nsga2.fast_non_dominated_sort(self.population.actual_population)
        for rank in ranks:
            self.nsga2.crowding_distance(rank)
        return ranks

    def solve(self):
        ranks = self.__start_problem()
        # NSGA2.print_ranks(ranks)
        for i in range(self.population.generations):
            population_for_crossover = self.common_operators.binary_tournament_selection(self.population.actual_population)
            population_childs = self.common_operators.crossover(population_for_crossover)
            first_child = population_childs[0]
            print(first_child)
            first_child.mutation_transposition()
            print(first_child)