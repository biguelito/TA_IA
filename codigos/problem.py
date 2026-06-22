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
        # Pontos encontrados com maximo e minimo de 100 execucoes, alterados em 0.2
        self.reference_points = {
            "eil51": {
                "max_point": (1144, 515),
                "min_point": (414, 4)
            },
            "berlin52": {
                "max_point": (21465, 10200),
                "min_point": (6592, 32)
            },
            "eil76": {
                "max_point": (),
                "min_point": ()
            },
            "rat99": {
                "max_point": (),
                "min_point": ()
            },
        }

    def get_nadir_point(self):
        return self.reference_points[self.instance_name]["max_point"]

    def get_min_point(self):
        return self.reference_points[self.instance_name]["min_point"]
