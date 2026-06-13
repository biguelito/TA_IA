from individual import Individual
from math import random

class CommonOperators:
    def __init__(self):
        pass

    def binary_tournament(self, population : list[Individual]) -> list[Individual]:
        selection : list
        choosed : Individual

        for i in range(len(population)):
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
    
    def binary_tournament_selection(self, population : list[Individual]):
        random_arragement_first_half = random.sample(population, k=len(population))
        selection_first_half = self.binary_tournament(random_arragement_first_half)
        random_arragement_second_half = random.sample(population, k=len(population))
        selection_second_half = self.binary_tournament(random_arragement_second_half)
        return selection_first_half + selection_second_half
