from solver import Solver

if __name__ == "__main__":
    solver = Solver()
    result_a = solver.solve("eil51", save=False)
    result_b = solver.solve("eil51", save=False, rebalance_by_centroid=0.8)

    comparison = solver.compare_pareto_metrics(result_a, result_b)