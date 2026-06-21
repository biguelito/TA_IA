import tsplib95

class Problem:
    def __init__(self, instance_name : str, salesman_quantity : int):
        self.instance_name = instance_name
        self.instance = tsplib95.load(f"problems/{instance_name}.tsp")
        self.salesman_quantity = salesman_quantity
        self.all_nodes = list(self.instance.get_nodes())
        self.first_node = self.all_nodes[0]
        self.nodes = list(self.all_nodes)
        self.nodes.remove(self.first_node)
        self.nodes_quantity = len(self.nodes)
        
        self.nadir_point = {
            "eil51": (1144, 515),
            "berlin52": (18233, 10200),
            "eil76": (0 , 0),
            "rat99": (0 , 0),
        }

    def get_nadir_point(self):
        return self.nadir_point[self.instance_name]