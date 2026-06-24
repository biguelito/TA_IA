from solver import Solver

if __name__ == "__main__":
    solver = Solver()
    # result_a = solver.solve("eil51", save=False)
    # result_b = solver.solve("eil51", save=False, rebalance_by_centroid=1)
    # comparison = solver.compare_pareto_metrics(result_a, result_b)

    # solver.run_centroid_experimental("eil51")

    # solver.run_centroid_screening("eil51", screening_runs=2, screening_values=[0.3, 0.5, 0.8])
    solver.run_centroid_final_comparison("eil51", final_runs=2, base_seed=44, selected_rebalance_by_centroid=0.8)