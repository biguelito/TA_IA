
def create_initial_population(qp):
    return [[0] * qp]

def binary_tournament_selection():
    return

def NSGA2(p0, n, mp):
    pn = None
    i = 0
    pi = p0
    while i < n:
        crossover_set = binary_tournament_selection(pi)
        ++i

    return pn

if __name__ == "__main__":
    qp = 100
    mp = 0.05
    n = 1000 
    p0 = create_initial_population(qp)

    
    NSGA2(p0, n, mp)
