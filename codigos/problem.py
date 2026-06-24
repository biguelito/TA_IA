import tsplib95

class Problem:
    def __init__(self, 
                 instance_name : str,
                 salesman_quantity : int,
                 iterations : int):
        self.instance_name = instance_name
        self.instance = tsplib95.load(f"problems/{instance_name}.tsp")
        self.salesman_quantity = salesman_quantity
        self.all_nodes = list(self.instance.get_nodes())
        self.first_node = self.all_nodes[0]
        self.nodes = list(self.all_nodes)
        self.nodes.remove(self.first_node)
        self.nodes_quantity = len(self.nodes)
        self.iterations = iterations
        # Pontos encontrados com maximo e minimo de 100 execucoes, alterados em 0.3
        self.reference_points = {
            "eil51": {
                "max_point": (1239, 558),
                "min_point": (362, 0)
            },
            "berlin52": {
                "max_point": (23254, 11050),
                "min_point": (5768, 0)
            },
            "eil76": {
                "max_point": (1475, 908),
                "min_point": (355, 0)
            },
            "rat99": {
                "max_point": (4591, 1904),
                "min_point": (1079, 0)
            },
        }

    def get_nadir_point(self):
        return self.reference_points[self.instance_name]["max_point"]

    def get_min_point(self):
        return self.reference_points[self.instance_name]["min_point"]
