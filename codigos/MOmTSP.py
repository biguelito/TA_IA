import random
import tsplib95

def create_initial_population(qp):
    return [[0] * qp]

def binary_tournament_selection():
    return

def crossover (crossover_set):
    return crossover_set

def mutation1(pk):
    return pk

def mutation2(pk):
    return pk

def fastNonDominatedSort(ri):
    return [ri[:len(ri)//2] , ri[len(ri)//2:]]

def crowding_distance_assignment(fj):
    return fj

def sort(fj):
    return

def NSGA2(p0, n, mp):
    pn = None
    i = 0
    pi = p0
    while i < n:
        crossover_set = binary_tournament_selection(pi)
        qi = crossover(crossover_set)
        
        for pk in qi:
            if (random.uniform(0, 1) <= mp):
                pk_muted = None
                if (random.uniform(0, 1) <= 0.5): 
                    pk_muted = mutation1(pk)
                else:
                    pk_muted = mutation2(pk)
            pk = pk_muted

        ri = pi + qi
        f = fastNonDominatedSort(ri)

        pii, j =  [], 0
        while len(pii) + len(f) <= len(p0):
            pii.append(f[j])
            j += 1

        fj = crowding_distance_assignment(f[j])
        fj = sort(fj)
        pii += fj[0 : (len(p0) - len(pii))]

        i += 1

    return pn

def load_problem(name, qtsp):
    problem = tsplib95.load(f"problems/{name}.tsp")
    return problem, len(list(problem.get_nodes())) + (qtsp-1)

if __name__ == "__main__":
    problem = load_problem("eil51", 7)

    qp = 100
    mp = 0.05
    n = 1000 

    p0 = create_initial_population(qp)
    # pn = NSGA2(p0, n, mp)

    print(problem.get_weight(1,2))