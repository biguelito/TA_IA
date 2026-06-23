from solver import Solver
from plotter import Plotter
from problem import Problem
from individual import Individual
from operators import Operators

import time

def test_rebalance_by_centroid():
    problem = Problem("eil51", 7, 1400)
    plotter = Plotter(problem)

    # previous_path = "31-8-26-7-43-24-23-48-27-32-11-38-16-9-49-5-37-17-4-47-12-46-51-6-14-25-18-13-41-40-19-42-44-15-45-33-10-39-30-34-50-2-29-21-20-35-36-3-28-22-8-16-21-26-32-41"
    previous_path = "26-7-23-43-24-14-25-13-41-19-40-42-44-15-37-17-4-18-47-12-46-51-27-32-11-5-38-30-34-50-16-9-49-10-39-33-45-21-29-2-20-35-36-3-28-31-8-22-48-6-24-44-46-47-48-49"
    individual_solution = Individual(problem)
    individual_solution.create_previous_chromossome(previous_path)
    plotter.plot_individual(individual_solution,
                            show_centroids=True,
                            save_path=f"solucoes/{(int(time.time()))}-previous_path_saida_before.png"
    )

    Operators(problem).rebalance_by_centroid(individual_solution, mode="expand_shortest")
    plotter.plot_individual(individual_solution,
                            show_centroids=True,
                            save_path=f"solucoes/{(int(time.time()))}-previous_path_saida_after.png"
    )


def find_nadir():
    solver = Solver()
    # solver.find_aproximate_nadir_point("eil51", 100)
    # solver.find_aproximate_nadir_point("berlin52_1", 100)
    # solver.find_aproximate_nadir_point("berlin52_2", 100)
    solver.find_aproximate_nadir_point("eil76_1", 100)
    # solver.find_aproximate_nadir_point("eil76_2", 100)
    # solver.find_aproximate_nadir_point("rat99", 100)
    return

if __name__ == "__main__":
    solver = Solver()
    result_a = solver.solve("eil51")
    result_b = solver.solve("eil51", rebalance_by_centroid=0.8)

    comparison = solver.compare_pareto_metrics(result_a, result_b)
    print(comparison)