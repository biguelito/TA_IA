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

    def create_random_salesman_division(self):
        division = []
        last_salesman = 0
        for div in range(self.problem.salesman_quantity-1):
            position = random.randint(last_salesman+1, self.problem.nodes_quantity-self.problem.salesman_quantity+div+1)
            last_salesman = position
            division.append(position)
        return division

    def create_costs(self):
        self.separate_salemans()
        self.calculate_paths_cost()
        self.calculate_functions()

    def create_random(self):
        self.paths = random.sample(self.problem.nodes, k=self.problem.nodes_quantity)
        self.divisions = self.create_random_salesman_division()
        self.create_costs()

    def create_crossover(self, paths, divisions):
        self.paths = paths
        self.divisions = divisions
        self.create_costs()

    def calculate_paths_cost(self):
        for path in self.salesman_paths:
            self.total_per_salesman.append(self.path_cost(path))

    def separate_salemans(self):
        start = 0
        ends = self.divisions + [len(self.paths)]
        for end in ends:
            salesman_path = self.paths[start : end]
            self.salesman_paths.append(salesman_path)
            start = end

    def calculate_functions(self):
        self.total_distance = sum(self.total_per_salesman)
        self.difference_longest_shortest = max(self.total_per_salesman) - min(self.total_per_salesman)

    def path_cost(self, path : list[int]):
        salesman_path_complete = [self.problem.first_node] + path + [self.problem.first_node]
        cost = 0
        for point in range(len(salesman_path_complete)-1):
            cost += self.problem.instance.get_weight(salesman_path_complete[point], salesman_path_complete[point+1])
        return cost

    @property    
    def chromossome(self):
        return self.paths + self.divisions
    
    def set_functions(self, total_distance, difference):
        self.total_distance = total_distance
        self.difference_longest_shortest = difference

    def print_paths(self):
        start = 0
        ends = self.divisions + [len(self.paths)]
        for i,end in enumerate(ends):
            print(f"{i}: {self.problem.first_node} - {' - '.join(str(chro) for chro in self.paths[start : end])} - {self.problem.first_node}")
            start = end

    def __str__(self):
        return '-'.join(str(chro) for chro in self.paths)
    
    def __repr__(self):
        return f"({self.total_distance},{self.difference_longest_shortest})"
        