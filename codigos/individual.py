import random

class Individual:
    def __init__(self, salesman_quantity, nodes_quantity):
        self.paths = None
        self.divisions = None
        self.salesman_quantity = salesman_quantity
        self.nodes_quantity = nodes_quantity

        self.total_distance = None
        self.difference_longest_shortest = None
        self.rank = None
        self.crowding_distance = 0

    def create_random_salesman_division(self):
        division = []
        last_salesman = 0
        for div in range(self.salesman_quantity-1):
            position = random.randint(last_salesman+1, self.nodes_quantity-self.salesman_quantity+div+1)
            last_salesman = position
            division.append(position)
        return division
    
    def create_random(self, nodes):
        self.paths = random.sample(nodes, k=len(nodes))
        self.divisions = self.create_random_salesman_division()

    @property    
    def chromossome(self):
        return self.paths + self.divisions
    
    def print_paths(self):
        start = 0
        for i in range(self.salesman_quantity-1):
            div = self.divisions[i]
            print(f"{i}: 0 - {' - '.join(str(chro) for chro in self.paths[start : div])} - 0")
            start = div
        print(f"{i+1}: 0 - {' - '.join(str(chro) for chro in self.paths[start : ])} - 0")