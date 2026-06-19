from solver import Solver
from individual_plotter import IndividualPlotter
from problem import Problem
from individual import Individual
from common_operators import CommonOperators

import random

def test_rebalance_by_centroid():
    problem = Problem("eil51", 7)
    plotter = IndividualPlotter(problem)

    previous_path = "51-46-12-47-18-14-25-13-41-40-42-19-4-17-37-44-15-45-33-39-10-30-34-50-9-49-5-38-11-16-21-29-20-35-36-3-28-31-8-26-48-23-7-43-24-6-27-32-22-2-29-40-46-47-48-49"
    individual_solution = Individual(problem)
    individual_solution.create_previous_chromossome(previous_path)
    plotter.plot_individual(individual_solution, show_centroids=True, save_path="solucoes/previous_path_saida_before.png")

    CommonOperators(problem).rebalance_by_centroid(individual_solution, mode="shrink_longest")
    plotter.plot_individual(individual_solution, show_centroids=True, save_path="solucoes/previous_path_saida_after.png")


if __name__ == "__main__":
    random.seed(42)

    test_rebalance_by_centroid()
