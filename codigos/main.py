from solver import Solver
from individual_plotter import IndividualPlotter
from problem import Problem
from individual import Individual
from common_operators import CommonOperators

import random

def test_rebalance_by_centroid():
    problem = Problem("eil51", 7)
    plotter = IndividualPlotter(problem)

    previous_path = "31-8-26-7-43-24-23-48-27-32-11-38-16-9-49-5-37-17-4-47-12-46-51-6-14-25-18-13-41-40-19-42-44-15-45-33-10-39-30-34-50-2-29-21-20-35-36-3-28-22-8-16-21-26-32-41"
    individual_solution = Individual(problem)
    individual_solution.create_previous_chromossome(previous_path)
    plotter.plot_individual(individual_solution, show_centroids=True, save_path="solucoes/previous_path_saida_before.png")

    CommonOperators(problem).rebalance_by_centroid(individual_solution, mode="expand_shortest")
    plotter.plot_individual(individual_solution, show_centroids=True, save_path="solucoes/previous_path_saida_after.png")


if __name__ == "__main__":
    random.seed(42)

    test_rebalance_by_centroid()
