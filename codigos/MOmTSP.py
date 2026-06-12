import random

from individual import Individual
from nsga2 import NSGA2
from problem import Problem

def pseudo_code(population_0, iterations, mutation_probability):
    population_size = len(population_0)
    iteration_counter = 0
    population_iteration = population_0
    while iteration_counter < iterations:
        population_crossover = binary_tournament_selection(population_iteration)
        population_childs = crossover(population_crossover)
        
        for child in population_childs:
            if (random.uniform(0, 1) <= mutation_probability):
                child_mutated = None
                if (random.uniform(0, 1) <= 0.5): 
                    child_mutated = mutation_inversion(child)
                else:
                    child_mutated = mutation_fragment(child)
            child = child_mutated

        population_complete = population_iteration + population_childs
        population_ranked = fast_non_dominated_sort(population_complete)

        population_next_interation = []
        rank = 0
        while len(population_next_interation) + len(population_ranked) <= len(population_size):
            population_next_interation.append(population_ranked[rank])
            rank += 1

        rank_sorted_crowding_distance = crowding_distance_assignment(population_ranked[rank])
        rank_sorted_crowding_distance = sort(rank_sorted_crowding_distance)
        population_next_interation += rank_sorted_crowding_distance[0 : (len(population_size) - len(population_next_interation))]
        population_iteration = list(population_next_interation)
        iteration_counter += 1

    return population_iteration

def create_initial_population(population_size : int, problem : Problem):
    population_0 = []
    for _ in range(population_size):
        individual = Individual()
        individual.create_random(problem)
        population_0.append(individual)
    return population_0

def binary_tournament_selection():
    return

def crossover (crossover_set):
    return crossover_set

def mutation_inversion(pk):
    return pk

def mutation_fragment(pk):
    return pk

def fast_non_dominated_sort(population):
    return [population[:len(population)//2] , population[len(population)//2:]]

def crowding_distance_assignment(fj):
    return fj

def sort(fj):
    return

def print_ranks(ranks):
    for i, rank in enumerate(ranks):
        print(f"rank {i+1}: {len(rank)} individuos")
        individual : Individual
        for individual in rank:
            print(f"{individual.rank} - {individual.crowding_distance} | f1 {individual.total_distance} - f2 {individual.difference_longest_shortest}", end=" | ")
            print(f"cost per path {' - '.join(str(t) for t in individual.total_per_salesman)}")

if __name__ == "__main__":
    salesman_quantity = 7
    problem = Problem("eil51", salesman_quantity)
    
    gene_size = len(problem.nodes) + (salesman_quantity-1)
    population_size = 10
    mutation_probability = 0.05
    iterations = 10

    population_0 = create_initial_population(population_size, problem)
    nsga2 = NSGA2()
    ranks = nsga2.fast_non_dominated_sort(population_0)
    for rank in ranks:
        nsga2.crowding_distance(rank)
    print_ranks(ranks)