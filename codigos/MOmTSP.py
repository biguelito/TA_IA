import random
import tsplib95

def create_initial_population(population_size, gene_size, salesman):
    return [[0] * qp]

def binary_tournament_selection():
    return

def crossover (crossover_set):
    return crossover_set

def mutation_inversion(pk):
    return pk

def mutation_fragment(pk):
    return pk

def fast_non_dominated_sort(ri):
    return [ri[:len(ri)//2] , ri[len(ri)//2:]]

def crowding_distance_assignment(fj):
    return fj

def sort(fj):
    return

def NSGA2(population_0, iterations, mutation_probability):
    pn = None
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
    gene_size = len(list(problem.get_nodes())) + (qtsp-1)
    return problem, gene_size

if __name__ == "__main__":
    salesman = 7
    problem, gene_size = load_problem("eil51", salesman)
    population_size = 100
    mutation_probability = 0.05
    iterations = 10

    population_0 = create_initial_population(population_size, gene_size, salesman)
    pn = NSGA2(population_0, iterations, mutation_probability)

    print(problem.get_weight(1,2))