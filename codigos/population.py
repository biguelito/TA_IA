from problem import Problem
from individual import Individual

class Population:
    def __init__(self, generations : int, population_size : int):
        self.generations = generations
        self.population_size = population_size
        self.actual_generation = 0
        self.actual_population : list[Individual]
        self.actual_population = None

    def create_initial_population(self, problem : Problem) -> list[Individual]:
        population_0 = []
        for _ in range(self.population_size):
            individual = Individual()
            individual.create_random(problem)
            population_0.append(individual)
        self.actual_population = population_0