import random
import tsplib95

from individual import Individual

def create_initial_population(population_size, nodes, salesman):
    population_0 = []
    nodes_quantity = len(nodes)
    for _ in range(population_size):
        individual = Individual(salesman, nodes_quantity)
        individual.create_random(nodes)
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

def NSGA2(population_0, iterations, mutation_probability, salesman):
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

def load_problem(name, qtsp):
    problem = tsplib95.load(f"problems/{name}.tsp")
    return problem

if __name__ == "__main__":
    salesman = 7
    problem = load_problem("eil51", salesman)
    gene_size = len(list(problem.get_nodes())) + (salesman-1)
    population_size = 1
    mutation_probability = 0.05
    iterations = 10

    population_0 = create_initial_population(population_size, list(problem.get_nodes()), salesman)
    print(population_0[0].chromossome)
    # pn = NSGA2(population_0, iterations, mutation_probability, salesman)