from individual import Individual
from problem import Problem
from plotter import Plotter

import random
import time
from shapely.geometry import Polygon

class Result:
    def __init__(self, problem : Problem, solutions : list[Individual], iterations : int):
        self.problem = problem
        self.solutions = solutions
        self.plotter = Plotter(problem)
        moment = str(int(time.time()))
        self.path = f"./solucoes/{moment}-{self.problem.instance_name}-{iterations}-{self.problem.salesman_quantity}"
        return
    
    def save_result(self,
        total_exec_time : float,
        iterations : int,
        salesman_quantity : int
    ):
        with open(f"{self.path}-solucoes.txt", "w") as f:
            f.write(f"{self.problem.instance_name} - {iterations} - {salesman_quantity} - {total_exec_time}:\n")
            for s in self.solutions:
                f.write(f"{s.id}: {s}\n")
        
        solution = random.sample(self.solutions, k=1)[0]
        self.plotter.plot_individual(solution, show_centroids=True, save_path=f"{self.path}-individual.png", show_plot=False)

        return
    
    def evaluate_pareto(self):
        nadir_point = self.problem.get_nadir_point()
        vertices = [(solution.total_distance, solution.difference_longest_shortest) for solution in self.solutions]
        vertices.append(nadir_point)
        polygon = Polygon(vertices) 
        hypervolume = polygon.area

        self.plotter.plot_pareto_front(self.solutions, 
            save_path=f"{self.path}-pareto.png",
            show_plot=True,
            max_point=nadir_point,
            hypervolume=hypervolume)