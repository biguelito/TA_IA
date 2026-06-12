import tsplib95

class Problem:
    def __init__(self, instance : str, salesman_quantity : int):
        self.instance = tsplib95.load(f"problems/{instance}.tsp")
        self.salesman_quantity = salesman_quantity
        self.all_nodes = list(self.instance.get_nodes())
        self.first_node = self.all_nodes[0]
        self.nodes = list(self.all_nodes)
        self.nodes.remove(self.first_node)
        self.nodes_quantity = len(self.nodes)