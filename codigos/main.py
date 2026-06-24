from solver import Solver

if __name__ == "__main__":
    solver = Solver()
    # result_a = solver.solve("eil51", save=True)
    # result_b = solver.solve("eil51", save=True, rebalance_by_centroid=0.8)
    # comparison = solver.compare_pareto_metrics(result_a, result_b)

    solver.run_centroid_experiment("eil51", save_all=True)
    solver.run_centroid_experiment("berlin52_1", save_all=True)
    solver.run_centroid_experiment("berlin52_2", save_all=True)
    solver.run_centroid_experiment("eil76_1", save_all=True)
    solver.run_centroid_experiment("eil76_2", save_all=True)
    solver.run_centroid_experiment("rat99", save_all=True)