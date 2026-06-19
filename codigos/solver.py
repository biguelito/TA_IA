from problem import Problem
from momtsp import MOmTSP
from individual import Individual

import timeit
import time

class Solver:
    def __init__(self):    
        self.repetitions = 10
        self.mutation_probability = 0.05
        self.population_size = 100
        return

    def __solve_problem(self, instance, population_size, mutation_probability, iterations, salesman_quantity, repetitions) -> tuple[float, list[Individual]]:
        problem = Problem(instance, salesman_quantity)

        momtsp = MOmTSP(problem,
                        population_size=population_size, 
                        mutation_probability=mutation_probability,
                        iterations=iterations)
        total_exec_time = timeit.timeit(lambda: momtsp.solve_repetitions(repetitions), number=1) 
        solutions = momtsp.best_solutions 
        self.__record_result(solutions=solutions,
            total_exec_time=total_exec_time,
            iterations=iterations,
            salesman_quantity=salesman_quantity,
            instance=instance)
        return total_exec_time, solutions
    
    def __record_result(self, solutions : list[Individual], total_exec_time, iterations, salesman_quantity, instance):
        with open(f"./solucoes/{str(int(time.time()))}-{instance}-{iterations}-{salesman_quantity}.txt", "w") as f:
            f.write(f"eil51 - {iterations} - {salesman_quantity} - {total_exec_time}:\n")
            for s in solutions:
                f.write(f"{s.id}: {s}\n")
        return

    def solve_eil51(self, iterations=1400, salesman_quantity=7) -> list[Individual]:
        total_exec_time, solutions = self.__solve_problem(
            instance="eil51", 
            population_size=self.population_size, 
            mutation_probability=self.mutation_probability, 
            iterations=iterations, 
            salesman_quantity=salesman_quantity, 
            repetitions=self.repetitions)
        return total_exec_time, solutions
    
    def solve_eil76(self, iterations=1800, salesman_quantity=7) -> list[Individual]:
        total_exec_time, solutions = self.__solve_problem(
            instance="eil76", 
            population_size=self.population_size, 
            mutation_probability=self.mutation_probability, 
            iterations=iterations, 
            salesman_quantity=salesman_quantity, 
            repetitions=self.repetitions)
        
        return total_exec_time, solutions
    
    def solve_berlin52(self, iterations=1400, salesman_quantity=5):
        total_exec_time, solutions = self.__solve_problem(
            instance="berlin52", 
            population_size=self.population_size, 
            mutation_probability=self.mutation_probability, 
            iterations=iterations, 
            salesman_quantity=salesman_quantity, 
            repetitions=self.repetitions)
        
        return total_exec_time, solutions
    
    def solve_rat99(self, iterations=2200, salesman_quantity=7):
        total_exec_time, solutions = self.__solve_problem(
            instance="rat99", 
            population_size=self.population_size, 
            mutation_probability=self.mutation_probability, 
            iterations=iterations, 
            salesman_quantity=salesman_quantity, 
            repetitions=self.repetitions)

        return total_exec_time, solutions
