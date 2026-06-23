from individual import Individual
from problem import Problem
from plotter import Plotter
from basic_operations import BasicOperations

import random
import time
from shapely.geometry import Polygon

class Result:
    def __init__(self,
                 problem : Problem,
                 solutions : list[Individual],
                 iterations : int,
                 total_exec_time : float,
                 rebalance_by_centroid : float | None = None):
        self.problem = problem
        self.solutions = sorted(solutions, key=lambda individual: (individual.total_distance, individual.difference_longest_shortest))
        self.plotter = Plotter(problem)
        moment = str(int(time.time()))
        self.path = f"./solucoes/{moment}-{self.problem.instance_name}-{iterations}-{self.problem.salesman_quantity}"
        self.total_exec_time = total_exec_time

        self.basic_operations = BasicOperations(problem)
        self.hypervolume = 0
        self.spacing = 0
        self.spreading = 0
        self.used_centroid = rebalance_by_centroid != None
        return
    
    def save_result(self, 
                    show_individual : bool = False,
                    show_pareto : bool = False):
        with open(f"{self.path}-solucoes.txt", "w") as f:
            f.write(f"{self.problem.instance_name}{" with centroid" if self.used_centroid else ""} - {self.problem.iterations} - {self.problem.salesman_quantity} - {self.total_exec_time}:\n")
            for s in self.solutions:
                f.write(f"{s.id}: {s}\n")

            f.write(f"hypervolume: {self.hypervolume}\n")
            f.write(f"spacing: {self.spacing}\n")
            f.write(f"spreading: {self.spreading}\n")

        solution = random.sample(self.solutions, k=1)[0]
        self.plotter.plot_individual(solution, show_centroids=True, save_path=f"{self.path}-individual.png", show_plot=show_individual, used_centroid=self.used_centroid)
        
        nadir_point = self.problem.get_nadir_point()
        min_point = self.problem.get_min_point()
        self.plotter.plot_pareto_front(self.solutions, 
            save_path=f"{self.path}-pareto.png",
            show_plot=show_pareto,
            max_point=nadir_point,
            min_point=min_point,
            hypervolume=self.hypervolume,
            spacing=self.spacing,
            spreading=self.spreading,
            used_centroid=self.used_centroid)

        return
    
    def evaluate_pareto(self):
        nadir_point = self.problem.get_nadir_point()
        vertices = [(solution.total_distance, solution.difference_longest_shortest) for solution in self.solutions]
        polygon_vertices = list(vertices)
        polygon_vertices.append(nadir_point)
        polygon = Polygon(polygon_vertices) 
        self.hypervolume = polygon.area
        self.spacing = self.basic_operations.calculate_spacing(vertices)
        self.spreading = self.basic_operations.calculate_spreading(vertices)