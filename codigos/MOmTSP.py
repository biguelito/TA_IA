from problem import Problem
from nsga2 import NSGA2
from population import Population
from common_operators import CommonOperators

import random
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

    def __start_population(self):
        self.population.create_initial_population(self.problem)
        ranks = self.nsga2.fast_non_dominated_sort(self.population.actual_population)
        for rank in ranks:
            self.nsga2.crowding_distance(rank)
        return

    def solve(self):
        self.__start_population()
        for i in range(self.population.generations):
            population_for_crossover = self.common_operators.binary_tournament_selection(self.population.actual_population)
            self.population.actual_childs = self.common_operators.crossover(population_for_crossover)
    
            for child in self.population.actual_childs:
                if (random.uniform(0, 1) <= self.mutation_probability):
                    if (random.uniform(0, 1) <= 0.5): 
                        child.mutation_inversion()
                    else:
                        child.mutation_transposition()

            population_ranked = self.nsga2.fast_non_dominated_sort(self.population.population_complete)
            
            population_next_generation = []
            rank = 0
            while len(population_next_generation) + len(population_ranked[rank]) <= self.population.population_size:
                population_next_generation += population_ranked[rank]
                rank += 1

            last_rank = population_ranked[rank]
            self.nsga2.crowding_distance(last_rank)
            last_rank.sort(reverse=True, key=lambda x: x.crowding_distance) 
            population_next_generation += last_rank[0 : (self.population.population_size - len(population_next_generation))]
            
            self.population.prepare_next_generation(population_next_generation)
        
        return self.population.result_individuals

        
        