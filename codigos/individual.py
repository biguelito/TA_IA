import random

from problem import Problem

class Individual:
    def __init__(self, problem : Problem):
        self.problem = problem
        self.paths = None
        self.divisions = None
        self.total_per_salesman = []
        self.salesman_paths = []

        self.total_distance = 0.0
        self.difference_longest_shortest = 0.0
        self.rank = 0
        self.crowding_distance = 0.0

        self.domination_count = 0
        self.dominated_solutions = []

    def __create_random_salesman_division(self):
        division = []
        last_salesman = 0
        for div in range(self.problem.salesman_quantity-1):
            position = random.randint(last_salesman+1, self.problem.nodes_quantity-self.problem.salesman_quantity+div+1)
            last_salesman = position
            division.append(position)
        return division

    def __calculate_costs(self):
        self.total_per_salesman = []
        self.salesman_paths = []
        self.__separate_salemans()
        self.__calculate_paths_cost()
        self.__calculate_functions()

    def __calculate_paths_cost(self):
        for path in self.salesman_paths:
            self.total_per_salesman.append(self.__path_cost(path))

    def __separate_salemans(self):
        start = 0
        ends = self.divisions + [len(self.paths)]
        for end in ends:
            salesman_path = self.paths[start : end]
            self.salesman_paths.append(salesman_path)
            start = end

    def __calculate_functions(self):
        self.total_distance = sum(self.total_per_salesman)
        self.difference_longest_shortest = max(self.total_per_salesman) - min(self.total_per_salesman)

    def __path_cost(self, path : list[int]):
        salesman_path_complete = [self.problem.first_node] + path + [self.problem.first_node]
        cost = 0
        for point in range(len(salesman_path_complete)-1):
            cost += self.problem.instance.get_weight(salesman_path_complete[point], salesman_path_complete[point+1])
        return cost

    def create_random(self):
        self.paths = random.sample(self.problem.nodes, k=self.problem.nodes_quantity)
        self.divisions = self.__create_random_salesman_division()
        self.__calculate_costs()

    def create_crossover(self, paths, divisions):
        self.paths = paths
        self.divisions = divisions
        self.__calculate_costs()

    def create_crossover_random_divisions(self, paths):
        self.paths = paths
        self.divisions = self.__create_random_salesman_division()
        self.__calculate_costs()

    def mutation_inversion(self):
        pos_1 = random.randint(0, len(self.paths)-2)
        pos_2 = random.randint(pos_1, len(self.paths)-1)
        self.paths = self.paths[: pos_1] + list(reversed(self.paths[pos_1 : pos_2])) + self.paths[pos_2 :]
        self.divisions = self.__create_random_salesman_division()
        self.__calculate_costs()
        return 

    def mutation_transposition(self):
        pos_1 = random.randint(0, len(self.paths)-2)
        pos_2 = random.randint(pos_1, len(self.paths)-1)
        self.paths = self.paths[pos_1 : pos_2] + self.paths[: pos_1] + self.paths[pos_2 :]
        self.divisions = self.__create_random_salesman_division()
        self.__calculate_costs()
        return
        
    @property    
    def chromossome(self):
        return self.paths + self.divisions
    
    @property
    def decodified_paths(self):
        complete_path = []
        for path in self.salesman_paths:
            complete_path.append(self.problem.first_node)
            complete_path += path
        return complete_path

    @property
    def id(self):
        return f"({self.total_distance},{self.difference_longest_shortest},{self.rank},{self.crowding_distance})"
    
    def __str__(self):
        return '-'.join(str(chro) for chro in self.paths)
    
    def __repr__(self):
        return self.id

    def print_paths(self):
        start = 0
        ends = self.divisions + [len(self.paths)]
        for i,end in enumerate(ends):
            print(f"{i}: {self.problem.first_node} - {' - '.join(str(chro) for chro in self.paths[start : end])} - {self.problem.first_node}")
            start = end
