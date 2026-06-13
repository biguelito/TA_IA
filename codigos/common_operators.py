from individual import Individual
from problem import Problem

import random
import copy

class CommonOperators:
    def __init__(self, problem : Problem):
        self.problem = problem

    def __binary_tournament(self, population : list[Individual]) -> list[Individual]:
        selection = []
        choosed : Individual

        for i in range(0, len(population), 2):
            a = population[i]
            b = population[i+1]

            if (a.rank < b.rank):
                choosed = a

            elif (a.rank > b.rank):
                choosed = b

            else:
                if (a.crowding_distance > b.crowding_distance):
                    choosed = a
                else:
                    choosed = b

            selection.append(choosed)

        return selection
    
    def __rearrange_in_par(self, full_population : list[Individual]):
        return [(full_population[i], full_population[i+1]) for i in range(0, len(full_population), 2)]

    def binary_tournament_selection(self, population : list[Individual]):
        random_arragement_first_half = random.sample(population, k=len(population))
        selection_first_half = self.__binary_tournament(random_arragement_first_half)
        random_arragement_second_half = random.sample(population, k=len(population))
        selection_second_half = self.__binary_tournament(random_arragement_second_half)
        full_population = selection_first_half + selection_second_half
        return self.__rearrange_in_par(full_population)

    def __next_city(self, paths, city):
        position = paths.index(city)
        if position == len(paths)-1:
            return paths[0]

        return paths[position+1]

    def __crossover_codified(self, a : Individual, b : Individual):
        father_a = copy.deepcopy(a.paths)
        father_b = copy.deepcopy(b.paths)

        city = random.sample(father_a, k=1)[0]
        child_paths = [city]
        while len(father_a) > 1:
            next_a = self.__next_city(father_a, city)
            next_b = self.__next_city(father_b, city) 
            father_a.remove(city)
            father_b.remove(city)
            distance_city_next_a = self.problem.instance.get_weight(city, next_a)
            distance_city_next_b = self.problem.instance.get_weight(city, next_b)
            if distance_city_next_a < distance_city_next_b:
                city = next_a
            else:
                city = next_b
            child_paths.append(city)
            
        return child_paths

    def __crossover_decodified(self, a : Individual, b : Individual):
        return a, b

    def __choose_division_randoms(self, a : Individual, b : Individual):
        if (random.uniform(0, 1) <= 0.5): 
            return a.divisions
        else:
            return b.divisions

    def __crossover_first_child(self, a : Individual, b : Individual) -> Individual:
        child_paths = self.__crossover_codified(a, b)
        child_division = self.__choose_division_randoms(a, b)
        child = Individual(self.problem)
        child.create_crossover(child_paths, child_division)

        return child_paths + child_division

    def __crossover_second_child(self, a : Individual, b : Individual) -> Individual:
        return a

    def crossover(self, fathers_population : list[tuple[Individual, Individual]]) -> list[Individual]:
        childs = []
        for fathers in fathers_population:
            father_a, father_b = fathers[0], fathers[1]
            child_1 = self.__crossover_first_child(father_a, father_b)
            childs.append(child_1)
            child_2 = self.__crossover_second_child(father_a, father_b)
            childs.append(child_2)

        return childs