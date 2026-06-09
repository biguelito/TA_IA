import tsplib95

from individual import Individual

class Problem:
    def __init__(self, instance : str, salesman_quantity : int):
        self.instance = tsplib95.load(f"problems/{instance}.tsp")
        self.salesman_quantity = salesman_quantity
        self.all_nodes = list(self.instance.get_nodes())
        self.first_node = self.all_nodes[0]
        self.nodes = list(self.all_nodes)
        self.nodes.remove(self.first_node)
        self.nodes_quantity = len(self.nodes)

    def calculate_functions(self, individual : Individual) -> tuple[int, int]:
        total_per_salesman = [0] * self.salesman_quantity
        start = 0
        ends = individual.divisions + [len(individual.paths)]
        for i, end in enumerate(ends):
            salesman_path = [self.first_node] + individual.paths[start : end] + [self.first_node]
            cost = self.path_cost(salesman_path)
            total_per_salesman[i] = cost
            start = end

        total_distance = sum(total_per_salesman)
        difference = max(total_per_salesman) - min(total_per_salesman)
        return total_distance, difference

    def path_cost(self, path : list[int]):
        cost = 0
        for point in range(len(path)-1):
            cost += self.instance.get_weight(path[point], path[point+1])
        return cost