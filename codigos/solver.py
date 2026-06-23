from problem import Problem
from momtsp import MOmTSP
from individual import Individual
from plotter import Plotter
from result import Result

import json
import timeit
import time

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
                         rebalance_by_centroid : float | None = None
    ) -> Result:
        problem = Problem(instance, salesman_quantity, iterations)

        momtsp = MOmTSP(problem,
                        population_size=population_size, 
                        mutation_probability=mutation_probability,
                        iterations=iterations,
                        rebalance_by_centroid=rebalance_by_centroid)
        total_exec_time = timeit.timeit(lambda: momtsp.solve_repetitions(repetitions), number=1) 
        solutions = momtsp.best_solutions         
        result = Result(problem, solutions, iterations, total_exec_time, rebalance_by_centroid)

        return result
    
    def solve(self, instance, save=True, rebalance_by_centroid : float | None = None) -> Result:
        iterations = self.__variations[instance]["iterations"]
        salesman_quantity = self.__variations[instance]["salesman_quantity"]
        instance_problem = self.__variations[instance]["problem"]

        result = self.__solve_instance(
            instance=instance_problem, 
            population_size=self.__population_size, 
            mutation_probability=self.__mutation_probability, 
            iterations=iterations, 
            salesman_quantity=salesman_quantity, 
            repetitions=self.__repetitions, 
            rebalance_by_centroid=rebalance_by_centroid)
        
        result.evaluate_result()
        if (save):
            result.save_result()
        return result

    def compare_pareto_metrics(self, result_a: Result, result_b: Result, save : bool = True) -> dict:
        if result_a.problem.instance_name != result_b.problem.instance_name:
            raise ValueError("Pareto fronts must belong to the same problem instance for comparison.")
        if result_a.problem.salesman_quantity != result_b.problem.salesman_quantity:
            raise ValueError("Pareto fronts must use the same number of salesmen for comparison.")

        if result_a.hypervolume == 0 and result_a.spacing == 0 and result_a.spreading == 0:
            result_a.evaluate_result()
        if result_b.hypervolume == 0 and result_b.spacing == 0 and result_b.spreading == 0:
            result_b.evaluate_result()

        def better(metric_name: str, value_a: float, value_b: float) -> str:
            if value_a == value_b:
                return "tie"

            if metric_name == "hypervolume":
                return "result_a" if value_a > value_b else "result_b"
            if metric_name == "spacing":
                return "result_a" if value_a < value_b else "result_b"
            if metric_name == "spreading":
                return "result_a" if value_a < value_b else "result_b"

        comparison = {
            "problem": result_a.problem.instance_name,
            "salesman_quantity": result_a.problem.salesman_quantity,
            "iterations": result_a.problem.iterations,
            "result_a": {
                "hypervolume": result_a.hypervolume,
                "spacing": result_a.spacing,
                "spreading": result_a.spreading,
                "rebalance_by_centroid": result_a.rebalance_by_centroid
            },
            "result_b": {
                "hypervolume": result_b.hypervolume,
                "spacing": result_b.spacing,
                "spreading": result_b.spreading,
                "rebalance_by_centroid": result_b.rebalance_by_centroid
            },
            "better": {
                "hypervolume": better("hypervolume", result_a.hypervolume, result_b.hypervolume),
                "spacing": better("spacing", result_a.spacing, result_b.spacing),
                "spreading": better("spreading", result_a.spreading, result_b.spreading),
            }
        }

        score_a = sum(1 for winner in comparison["better"].values() if winner == "result_a")
        score_b = sum(1 for winner in comparison["better"].values() if winner == "result_b")

        if score_a == score_b:
            comparison["overall"] = "tie"
        else:
            comparison["overall"] = "result_a" if score_a > score_b else "result_b"

        if save:
            moment = str(int(time.time()))
            with open(f"./solucoes/{moment}-comparison.json", "w") as f:
                json.dump(comparison, f, indent=4)

        return comparison

    def find_aproximate_nadir_point(self, instance, loops):
        instance_problem = self.__variations[instance]["problem"]
        iterations = self.__variations[instance]["iterations"]
        salesman_quantity = self.__variations[instance]["salesman_quantity"]

        solutions : list[Individual]
        solutions = []
        total_time = 0
        for i in range(loops):
            result = self.__solve_instance(
                instance=instance_problem, 
                population_size=self.__population_size, 
                mutation_probability=self.__mutation_probability, 
                iterations=iterations, 
                salesman_quantity=salesman_quantity, 
                repetitions=self.__repetitions)
            
            solutions += result.solutions
            total_time += result.total_exec_time
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

        problem = Problem(instance_problem, salesman_quantity, iterations)
        plotter = Plotter(problem)
        plotter.plot_pareto_front(solutions, save_path=f"{path}-pareto.png", show_plot=False,max_point=max_point, min_point=min_point)
        
        print(f"completo {instance} - {loops} - {total_time}")
        return
