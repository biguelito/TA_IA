from problem import Problem
from momtsp import MOmTSP
from individual import Individual
from plotter import Plotter
from result import Result

import json
import random
import statistics
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

    def __solve_with_seed(self, instance: str, seed: int, rebalance_by_centroid: float | None = None) -> Result:
        random.seed(seed)
        return self.solve(instance, save=False, rebalance_by_centroid=rebalance_by_centroid)

    def __get_result_metrics(self, result: Result) -> dict:
        if len(result.execution_metrics) == 0:
            result.evaluate_result()

        return {
            "front_size": result.execution_metrics["front_size"],
            "best_total_distance": result.execution_metrics["best_total_distance"],
            "median_total_distance": result.execution_metrics["median_total_distance"],
            "mean_total_distance": result.execution_metrics["mean_total_distance"],
            "best_difference": result.execution_metrics["best_difference"],
            "median_difference": result.execution_metrics["median_difference"],
            "mean_difference": result.execution_metrics["mean_difference"],
            "hypervolume": result.execution_metrics["hypervolume"],
            "spacing": result.execution_metrics["spacing"],
            "spreading": result.execution_metrics["spreading"],
            "total_exec_time": result.execution_metrics["total_exec_time"],
        }

    def __metric_summary(self, values: list[float | int]) -> dict:
        return {
            "mean": statistics.fmean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
        }

    def __winner_for_metric(self, metric_name: str, baseline_value: float, centroid_value: float) -> str:
        if baseline_value == centroid_value:
            return "tie"

        if metric_name == "hypervolume":
            return "baseline" if baseline_value > centroid_value else "centroid"

        return "baseline" if baseline_value < centroid_value else "centroid"

    def __build_paired_run_record(self, seed: int, baseline_result: Result, centroid_result: Result) -> dict:
        baseline_metrics = self.__get_result_metrics(baseline_result)
        centroid_metrics = self.__get_result_metrics(centroid_result)
        metric_names = list(baseline_metrics.keys())
        comparison_metric_names = [
            "best_total_distance",
            "median_total_distance",
            "best_difference",
            "median_difference",
            "mean_difference",
            "hypervolume",
            "spacing",
            "spreading",
        ]

        return {
            "seed": seed,
            "baseline": baseline_metrics,
            "centroid": centroid_metrics,
            "delta": {
                metric_name: centroid_metrics[metric_name] - baseline_metrics[metric_name]
                for metric_name in metric_names
            },
            "better": {
                metric_name: self.__winner_for_metric(
                    metric_name,
                    baseline_metrics[metric_name],
                    centroid_metrics[metric_name]
                )
                for metric_name in comparison_metric_names
            }
        }

    def __summarize_protocol_stage(self, run_records: list[dict], rebalance_by_centroid: float) -> dict:
        metric_names = list(run_records[0]["baseline"].keys())
        comparison_metric_names = list(run_records[0]["better"].keys())

        return {
            "rebalance_by_centroid": rebalance_by_centroid,
            "runs": run_records,
            "summary": {
                "baseline": {
                    metric_name: self.__metric_summary([run["baseline"][metric_name] for run in run_records])
                    for metric_name in metric_names
                },
                "centroid": {
                    metric_name: self.__metric_summary([run["centroid"][metric_name] for run in run_records])
                    for metric_name in metric_names
                },
                "delta": {
                    metric_name: self.__metric_summary([run["delta"][metric_name] for run in run_records])
                    for metric_name in metric_names
                },
                "wins": {
                    metric_name: {
                        "baseline": sum(1 for run in run_records if run["better"][metric_name] == "baseline"),
                        "centroid": sum(1 for run in run_records if run["better"][metric_name] == "centroid"),
                        "tie": sum(1 for run in run_records if run["better"][metric_name] == "tie"),
                    }
                    for metric_name in comparison_metric_names
                }
            }
        }

    def __select_screening_winner(self, screening_results: list[dict]) -> dict:
        return min(
            screening_results,
            key=lambda screening_result: (
                screening_result["summary"]["centroid"]["median_difference"]["median"],
                screening_result["summary"]["centroid"]["best_difference"]["median"],
                -screening_result["summary"]["centroid"]["hypervolume"]["median"],
                screening_result["summary"]["delta"]["median_total_distance"]["median"],
            )
        )

    def __save_json_file(self, data: dict, file_suffix: str):
        moment = str(int(time.time()))
        with open(f"./solucoes/{moment}-{file_suffix}.json", "w") as f:
            json.dump(data, f, indent=4)

    def compare_pareto_metrics(self, result_a: Result, result_b: Result, save : bool = True) -> dict:
        if result_a.problem.instance_name != result_b.problem.instance_name:
            raise ValueError("Pareto fronts must belong to the same problem instance for comparison.")
        if result_a.problem.salesman_quantity != result_b.problem.salesman_quantity:
            raise ValueError("Pareto fronts must use the same number of salesmen for comparison.")

        if len(result_a.execution_metrics) == 0:
            result_a.evaluate_result()
        if len(result_b.execution_metrics) == 0:
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
                "hypervolume": result_a.execution_metrics["hypervolume"],
                "spacing": result_a.execution_metrics["spacing"],
                "spreading": result_a.execution_metrics["spreading"],
                "rebalance_by_centroid": result_a.rebalance_by_centroid
            },
            "result_b": {
                "hypervolume": result_b.execution_metrics["hypervolume"],
                "spacing": result_b.execution_metrics["spacing"],
                "spreading": result_b.execution_metrics["spreading"],
                "rebalance_by_centroid": result_b.rebalance_by_centroid
            },
            "better": {
                "hypervolume": better("hypervolume", result_a.execution_metrics["hypervolume"], result_b.execution_metrics["hypervolume"]),
                "spacing": better("spacing", result_a.execution_metrics["spacing"], result_b.execution_metrics["spacing"]),
                "spreading": better("spreading", result_a.execution_metrics["spreading"], result_b.execution_metrics["spreading"]),
            }
        }

        score_a = sum(1 for winner in comparison["better"].values() if winner == "result_a")
        score_b = sum(1 for winner in comparison["better"].values() if winner == "result_b")

        if score_a == score_b:
            comparison["overall"] = "tie"
        else:
            comparison["overall"] = "result_a" if score_a > score_b else "result_b"

        if save:
            self.__save_json_file(comparison, "comparison")

        return comparison

    def run_centroid_screening(
            self,
            instance: str = "eil51",
            screening_values: list[float] | None = None,
            screening_runs: int = 10,
            base_seed: int = 42,
            save: bool = True
    ) -> dict:
        if instance not in self.__variations:
            raise ValueError(f"Unknown instance variation '{instance}'.")

        if screening_values is None:
            screening_values = [0.05, 0.10, 0.20, 0.30, 0.50, 0.80, 1]

        variation = self.__variations[instance]
        screening_seeds = [base_seed + i for i in range(screening_runs)]

        screening_baseline_results = {
            seed: self.__solve_with_seed(instance, seed, rebalance_by_centroid=None)
            for seed in screening_seeds
        }

        screening_results = []
        for centroid_value in screening_values:
            centroid_results = {
                seed: self.__solve_with_seed(instance, seed, rebalance_by_centroid=centroid_value)
                for seed in screening_seeds
            }
            run_records = [
                self.__build_paired_run_record(
                    seed,
                    screening_baseline_results[seed],
                    centroid_results[seed]
                )
                for seed in screening_seeds
            ]
            screening_results.append(self.__summarize_protocol_stage(run_records, centroid_value))

        selected_screening = self.__select_screening_winner(screening_results)
        screening = {
            "instance_variation": instance,
            "problem": variation["problem"],
            "salesman_quantity": variation["salesman_quantity"],
            "iterations": variation["iterations"],
            "runs": screening_runs,
            "seeds": screening_seeds,
            "candidates": screening_results,
            "selection_rule": [
                "lowest median_difference median",
                "lowest best_difference median",
                "highest hypervolume median",
                "lowest median_total_distance delta median",
            ],
            "selected_rebalance_by_centroid": selected_screening["rebalance_by_centroid"],
        }

        if save:
            self.__save_json_file(screening, f"{instance}-screening")

        return screening

    def run_centroid_final_comparison(
            self,
            instance: str = "eil51",
            selected_rebalance_by_centroid: float | None = None,
            final_runs: int = 30,
            base_seed: int = 42,
            save: bool = True
    ) -> dict:
        if instance not in self.__variations:
            raise ValueError(f"Unknown instance variation '{instance}'.")
        if selected_rebalance_by_centroid is None:
            raise ValueError("selected_rebalance_by_centroid must be informed for the final comparison.")

        variation = self.__variations[instance]
        final_seeds = [base_seed + i for i in range(final_runs)]

        final_baseline_results = {
            seed: self.__solve_with_seed(instance, seed, rebalance_by_centroid=None)
            for seed in final_seeds
        }
        final_centroid_results = {
            seed: self.__solve_with_seed(instance, seed, rebalance_by_centroid=selected_rebalance_by_centroid)
            for seed in final_seeds
        }
        final_run_records = [
            self.__build_paired_run_record(
                seed,
                final_baseline_results[seed],
                final_centroid_results[seed]
            )
            for seed in final_seeds
        ]

        final_comparison = {
            "instance_variation": instance,
            "problem": variation["problem"],
            "salesman_quantity": variation["salesman_quantity"],
            "iterations": variation["iterations"],
            "runs": final_runs,
            "seeds": final_seeds,
            "rebalance_by_centroid": selected_rebalance_by_centroid,
            "results": self.__summarize_protocol_stage(final_run_records, selected_rebalance_by_centroid),
        }

        if save:
            self.__save_json_file(final_comparison, f"{instance}-final-comparison")

        return final_comparison

    def run_centroid_experimental(
            self,
            instance: str = "eil51",
            screening_values: list[float] | None = None,
            screening_runs: int = 10,
            final_runs: int = 30,
            base_seed: int = 42,
            save: bool = True
    ) -> dict:
        screening = self.run_centroid_screening(
            instance=instance,
            screening_values=screening_values,
            screening_runs=screening_runs,
            base_seed=base_seed,
            save=False
        )
        final_comparison = self.run_centroid_final_comparison(
            instance=instance,
            selected_rebalance_by_centroid=screening["selected_rebalance_by_centroid"],
            final_runs=final_runs,
            base_seed=base_seed + screening_runs,
            save=False
        )

        variation = self.__variations[instance]
        protocol = {
            "instance_variation": instance,
            "problem": variation["problem"],
            "salesman_quantity": variation["salesman_quantity"],
            "iterations": variation["iterations"],
            "screening": screening,
            "final_comparison": final_comparison,
        }

        if save:
            self.__save_json_file(protocol, f"{instance}-protocol")

        return protocol

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
