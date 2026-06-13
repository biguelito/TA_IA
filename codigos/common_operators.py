from individual import Individual
import random

class CommonOperators:
    def binary_tournament(population : list[Individual]) -> list[Individual]:
        selection = []
        choosed : Individual

        for i in range(0, len(population), 2):
            a = population[i]
            b = population[i+1]

            if (a.rank < b.rank):
                choosed = a

            elif (a.rank > b.rank):
                choosed = b

            else:
                if (a.crowding_distance > b.crowding_distance):
                    choosed = a
                else:
                    choosed = b

            selection.append(choosed)

        return selection
    
    def rearrange_in_par(full_population : list[Individual]):
        return [(full_population[i], full_population[i+1]) for i in range(0, len(full_population), 2)]

    def binary_tournament_selection(population : list[Individual]):
        random_arragement_first_half = random.sample(population, k=len(population))
        selection_first_half = CommonOperators.binary_tournament(random_arragement_first_half)
        random_arragement_second_half = random.sample(population, k=len(population))
        selection_second_half = CommonOperators.binary_tournament(random_arragement_second_half)
        full_population = selection_first_half + selection_second_half
        return CommonOperators.rearrange_in_par(full_population)
