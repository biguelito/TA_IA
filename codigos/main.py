from solver import Solver

if __name__ == "__main__":
    solver = Solver()
    
    # Roda experimento completo para todas as instancias, varias horas de execucao 
    # solver.run_complete_centroid_experiment(
    #     instance_variations=["eil51", "berlin52_1", "berlin52_2", "eil76_1", "eil76_2", "rat99"]
    # )
 
    # Soluciona um problema do caixeiro com alguns valores pre defninidos
    solver.solve("eil51")
    
    # Soluciona um problema do caixeiro com alguns valores pre defninidos
    # Aplica mutação por centroide com probabilidade desejada
    solver.solve("eil51", rebalance_by_centroid=0.2)