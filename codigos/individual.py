import random

from problem import Problem

class Individual:
    def __init__(self):
        self.paths = None
        self.divisions = None
        self.salesman_quantity = 0
        self.nodes_quantity = 0
        self.total_per_salesman = [0] * self.salesman_quantity
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
        for div in range(self.salesman_quantity-1):
            position = random.randint(last_salesman+1, self.nodes_quantity-self.salesman_quantity+div+1)
            last_salesman = position
            division.append(position)
        return division
    
    def create_random(self, problem : Problem):
        self.salesman_quantity = problem.salesman_quantity
        self.nodes_quantity = problem.nodes_quantity
        self.first_node = problem.first_node
        self.paths = random.sample(problem.nodes, k=self.nodes_quantity)
        self.divisions = self.create_random_salesman_division()
        self.separate_salemans()
        self.calculate_paths_cost(problem)
        self.calculate_functions()

    def calculate_paths_cost(self, problem : Problem):
        for path in self.salesman_paths:
            self.total_per_salesman.append(self.path_cost(problem, path))

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

    def path_cost(self, problem : Problem, path : list[int]):
        salesman_path_complete = [self.first_node] + path + [self.first_node]
        cost = 0
        for point in range(len(salesman_path_complete)-1):
            cost += problem.instance.get_weight(salesman_path_complete[point], salesman_path_complete[point+1])
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
            print(f"{i}: {self.first_node} - {' - '.join(str(chro) for chro in self.paths[start : end])} - {self.first_node}")
            start = end

    def __str__(self):
        return '-'.join(str(chro) for chro in self.paths)
    
    def __repr__(self):
        return f"({self.total_distance},{self.difference_longest_shortest})"
        