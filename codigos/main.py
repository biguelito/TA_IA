from solver import Solver

if __name__ == "__main__":
    solver = Solver()
 
    solver.run_complete_centroid_experiment(
        instance_variations=["eil51"],
        screening_values=[0.20, 0.80],
        screening_runs=2,
        final_runs=2,
        base_seed=42,
    )
