from solver import Solver

if __name__ == "__main__":
    solver = Solver()
 
    solver.run_complete_centroid_experiment(
        instance_variations=["eil51", "berlin52_1", "berlin52_2", "eil76_1", "eil76_2", "rat99"],
        final_runs=30
        save_all=True
    )
