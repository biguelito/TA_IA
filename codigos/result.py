from individual import Individual
from problem import Problem
from plotter import Plotter
from basic_operations import BasicOperations

import random
import statistics
import time
from pathlib import Path
from shapely.geometry import Polygon

class Result:
    def __init__(self,
                 problem : Problem,
                 solutions : list[Individual],
                 iterations : int,
                 total_exec_time : float,
                 rebalance_by_centroid : float | None = None,
                 output_dir: str | None = None):
        self.problem = problem
        self.solutions = sorted(solutions, key=lambda individual: (individual.total_distance, individual.difference_longest_shortest))
        self.plotter = Plotter(problem)
        moment = str(int(time.time()))
        self.output_dir = output_dir or "./solucoes"
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        self.path = str(Path(self.output_dir) / f"{moment}-{self.problem.instance_name}-{iterations}-{self.problem.salesman_quantity}")
        self.total_exec_time = total_exec_time

        self.basic_operations = BasicOperations(problem)
        self.execution_metrics = {}
        self.rebalance_by_centroid = rebalance_by_centroid
        return
    
    def save_result(self, 
                    show_individual : bool = False,
                    show_pareto : bool = False):
        with open(f"{self.path}-solucoes.txt", "w") as f:
            f.write(f"{self.problem.instance_name}{f" with centroid {self.rebalance_by_centroid}" if self.rebalance_by_centroid else ""} - {self.problem.iterations} - {self.problem.salesman_quantity} - {self.total_exec_time}:\n")
            for s in self.solutions:
                f.write(f"{s.id}: {s}\n")

            for metric_name, metric_value in self.execution_metrics.items():
                f.write(f"{metric_name}: {metric_value}\n")
            f.write(f"rebalance_by_centroid: {self.rebalance_by_centroid}\n")
            
        solution = random.sample(self.solutions, k=1)[0]
        self.plotter.plot_individual(solution, show_centroids=True, save_path=f"{self.path}-individual.png", show_plot=show_individual, rebalance_by_centroid=self.rebalance_by_centroid)
        
        nadir_point = self.problem.get_nadir_point()
        min_point = self.problem.get_min_point()
        self.plotter.plot_pareto_front(self.solutions, 
            save_path=f"{self.path}-pareto.png",
            show_plot=show_pareto,
            max_point=nadir_point,
            min_point=min_point,
            hypervolume=self.execution_metrics["hypervolume"],
            spacing=self.execution_metrics["spacing"],
            spreading=self.execution_metrics["spreading"],
            rebalance_by_centroid=self.rebalance_by_centroid)

        return
    
    def evaluate_result(self):
        nadir_point = self.problem.get_nadir_point()
        vertices = [(solution.total_distance, solution.difference_longest_shortest) for solution in self.solutions]
        polygon_vertices = list(vertices)
        polygon_vertices.append(nadir_point)
        polygon = Polygon(polygon_vertices) 

        total_distances = [solution.total_distance for solution in self.solutions]
        total_differences = [solution.difference_longest_shortest for solution in self.solutions]

        self.execution_metrics = {
            "front_size": len(self.solutions),
            "best_total_distance": min(total_distances),
            "median_total_distance": statistics.median(total_distances),
            "mean_total_distance": statistics.fmean(total_distances),
            "best_difference": min(total_differences),
            "median_difference": statistics.median(total_differences),
            "mean_difference": statistics.fmean(total_differences),
            "hypervolume": polygon.area,
            "spacing": self.basic_operations.calculate_spacing(vertices),
            "spreading": self.basic_operations.calculate_spreading(vertices),
            "total_exec_time": self.total_exec_time,
        }
