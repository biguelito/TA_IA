from problem import Problem
from nsga2 import NSGA2
from population import Population
from operators import Operators

import random

class MOmTSP:
    def __init__(self, 
            problem : Problem,
            population_size : int,
            mutation_probability : float,
            iterations : int,
            rebalance_by_centroid : float | None = None
    ):
        self.problem = problem        
        self.mutation_probability = mutation_probability
        self.population = Population(iterations, population_size)
        self.operators = Operators(problem)
        self.nsga2 = NSGA2()
        self.solutions_chromossome_for_filtering = set()
        self.unique_solutions = []
        self.ranked_unique_solutions = None

        self.rebalance_by_centroid = rebalance_by_centroid
        self.mutation_inversion_probability = (1-rebalance_by_centroid)/2 if rebalance_by_centroid else 0.5
        self.mutation_transposition_probability = 1-rebalance_by_centroid if rebalance_by_centroid else None
        return 

    def __save_unique_solutions(self, individuals):
        for individual in individuals:
            chromossome_key = tuple(individual.chromossome)
            if chromossome_key in self.solutions_chromossome_for_filtering:
                continue

            self.solutions_chromossome_for_filtering.add(chromossome_key)
            self.unique_solutions.append(individual)

    def __start_population(self):
        self.population.create_initial_population(self.problem)
        ranks = self.nsga2.fast_non_dominated_sort(self.population.actual_population)
        for rank in ranks:
            self.nsga2.crowding_distance(rank)
        return
    
    def __mutation_without_centroid(self, child):
        if (random.uniform(0, 1) <= self.mutation_inversion_probability): 
            child = self.operators.mutation_inversion(child)
        else:
            child = self.operators.mutation_transposition(child)

        return child

    def __mutation_with_centroid(self, child):
        probability = random.uniform(0, 1)
        if (probability <= self.mutation_inversion_probability): 
            child = self.operators.mutation_inversion(child)
        elif (probability <= self.mutation_transposition_probability):
            child = self.operators.mutation_transposition(child)
        else:
            child = self.operators.rebalance_by_centroid(child, "expand_shortest")
        
        return child

    def __mutation(self, child):
        if self.rebalance_by_centroid:
            child = self.__mutation_with_centroid(child)
        else:
            child = self.__mutation_without_centroid(child)

        return child

    def solve(self):
        self.__start_population()
        for i in range(self.population.generations):
            population_for_crossover = self.operators.binary_tournament_selection(self.population.actual_population)
            self.population.actual_childs = self.operators.crossover(population_for_crossover)
    
            for child in self.population.actual_childs:
                if (random.uniform(0, 1) <= self.mutation_probability):
                    child = self.__mutation(child)

            population_ranked = self.nsga2.fast_non_dominated_sort(self.population.population_complete)
            
            population_next_generation = []
            rank = 0
            while (
                rank < len(population_ranked)
                and len(population_next_generation) + len(population_ranked[rank]) <= self.population.population_size
            ):
                population_next_generation += population_ranked[rank]
                rank += 1

            if rank < len(population_ranked):
                last_rank = population_ranked[rank]
                self.nsga2.crowding_distance(last_rank)
                last_rank.sort(reverse=True, key=lambda x: x.crowding_distance) 
                population_next_generation += last_rank[0 : (self.population.population_size - len(population_next_generation))]
            
            self.population.prepare_next_generation(population_next_generation)

        best_solutions = self.population.result_individuals
        self.__save_unique_solutions(best_solutions)
        return best_solutions

    def solve_repetitions(self, repetitions):
        for i in range(repetitions):
            self.solve()
        return self.best_solutions

    @property
    def best_solutions(self):
        if self.ranked_unique_solutions is None:
            self.ranked_unique_solutions = self.nsga2.fast_non_dominated_sort(self.unique_solutions)[0]
            self.nsga2.crowding_distance(self.ranked_unique_solutions)
        return self.ranked_unique_solutions
    

