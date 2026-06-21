from problem import Problem
from momtsp import MOmTSP
from individual import Individual
from plotter import Plotter
from result import Result

import timeit
import time
import random

class Solver:
    def __init__(self):    
        self.__repetitions = 1
        self.__mutation_probability = 0.05
        self.__population_size = 100
        
        self.__variations = {
            "eil51": {
                "problem": "eil51",
                "salesman_quantity": 7,
                "iterations": 1400                
            }, 
            "berlin52_1": {
                "problem": "berlin52",
                "salesman_quantity": 5,
                "iterations": 1400                
            },
            "berlin52_2": {
                "problem": "berlin52",
                "salesman_quantity": 7,
                "iterations": 1400                
            },
            "eil76_1": {
                "problem": "eil76",
                "salesman_quantity": 3,
                "iterations": 1800                
            },
            "eil76_2": {
                "problem": "eil76",
                "salesman_quantity": 7,
                "iterations": 1800                
            },
            "rat99": {
                "problem": "rat99",
                "salesman_quantity": 7,
                "iterations": 2200                
            } 
        }

        return

    def __solve_instance(self,
                         instance : str,
                         population_size : int,
                         mutation_probability : float,
                         iterations : int,
                         salesman_quantity : int,
                         repetitions : int,
                         save=True
    ) -> tuple[float, list[Individual]]:
        problem = Problem(instance, salesman_quantity)

        momtsp = MOmTSP(problem,
                        population_size=population_size, 
                        mutation_probability=mutation_probability,
                        iterations=iterations)
        total_exec_time = timeit.timeit(lambda: momtsp.solve_repetitions(repetitions), number=1) 
        solutions = momtsp.best_solutions 
        
        solver_result = Result(problem, solutions, iterations)
        if (save):
            solver_result.save_result(total_exec_time=total_exec_time,
                iterations=iterations,
                salesman_quantity=salesman_quantity)
        solver_result.evaluate_pareto()
        return total_exec_time, solutions
    
    def solve(self, instance, save=True) -> tuple[float, list[Individual]]:
        iterations = self.__variations[instance]["iterations"]
        salesman_quantity = self.__variations[instance]["salesman_quantity"]
        instance_problem = self.__variations[instance]["problem"]

        total_exec_time, solutions = self.__solve_instance(
            instance=instance_problem, 
            population_size=self.__population_size, 
            mutation_probability=self.__mutation_probability, 
            iterations=iterations, 
            salesman_quantity=salesman_quantity, 
            repetitions=self.__repetitions, 
            save=save)
        return total_exec_time, solutions

    def find_near_nadir_point(self, instance, loops):
        instance_problem = self.__variations[instance]["problem"]
        iterations = self.__variations[instance]["iterations"]
        salesman_quantity = self.__variations[instance]["salesman_quantity"]

        solutions : list[Individual]
        solutions = []
        total_time = 0
        for i in range(loops):
            total_exec_time, solutions_loop = self.solve(instance, save=False)
            solutions += solutions_loop
            total_time += total_exec_time
            print(f"completado {i}")

        extreme_solutions = [indv for indv in solutions if indv.crowding_distance == float("inf")]
        total_distances = [indv.total_distance for indv in extreme_solutions]
        total_differences = [indv.difference_longest_shortest for indv in extreme_solutions]
        max_point = (max(total_distances), max(total_differences))
        min_point = (min(total_distances), min(total_differences))

        moment = str(int(time.time()))
        path = f"./solucoes/{moment}-{instance_problem}-{iterations}-{salesman_quantity}"
        with open(f"./{path}-nadir.txt", "w") as f:
            f.write(f"{instance_problem} - {iterations} - {salesman_quantity} - {total_time} - {loops}:\n")
            for s in solutions:
                f.write(f"{s.id}: {s}\n")
            f.write(f"max point ({max_point[0]}, {max_point[1]})\n")
            f.write(f"min point ({min_point[0]}, {min_point[1]})")

        problem = Problem(instance_problem, salesman_quantity)
        plotter = Plotter(problem)
        plotter.plot_pareto_front(solutions, save_path=f"{path}-pareto.png", show_plot=False,max_point=max_point, min_point=min_point)
        
        print(f"completo {instance} - {loops} - {total_time}")
        return