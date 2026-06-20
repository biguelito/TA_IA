from individual import Individual

class NSGA2:
    def __init__(self):
        pass

    def __a_dominates_b(self, a : Individual, b : Individual):
        better_or_equal_every = (
            a.total_distance <= b.total_distance 
            and a.difference_longest_shortest <= b.difference_longest_shortest
        )

        better_least_one = (
            a.total_distance < b.total_distance
            or a.difference_longest_shortest < b.difference_longest_shortest
        )

        return better_or_equal_every and better_least_one
    
    def fast_non_dominated_sort(self, population : list[Individual]) -> list[list[Individual]]:
        ranks = [[]]
        for a in population:
            a.domination_count = 0
            a.dominated_solutions = []
            a.rank = 0
            for b in population:
                if a is b:
                    continue

                if self.__a_dominates_b(a, b):
                    a.dominated_solutions.append(b)
                elif self.__a_dominates_b(b, a):
                    a.domination_count += 1

            if a.domination_count == 0:
                a.rank = 1
                ranks[0].append(a)

        i = 0
        while len(ranks[i]) > 0:
            next_front = []
            for a in ranks[i]:
                for b in a.dominated_solutions:
                    b.domination_count -= 1

                    if b.domination_count == 0:
                        b.rank = i + 2
                        next_front.append(b)
                        
            i += 1
            ranks.append(next_front)

        ranks.pop()
        return ranks
    
    def crowding_distance(self, rank : list[Individual]):
        if len(rank) == 0:
            return

        rank_size = len(rank)
        original_order = {individual: index for index, individual in enumerate(rank)}
        for individual in rank:
            individual.crowding_distance = 0

        min_total_distance = min(individual.total_distance for individual in rank)
        min_difference = min(individual.difference_longest_shortest for individual in rank)

        total_distance_extreme = min(
            (individual for individual in rank if individual.total_distance == min_total_distance),
            key=lambda individual: original_order[individual]
        )
        difference_extreme = min(
            (
                individual for individual in rank
                if individual.difference_longest_shortest == min_difference
            ),
            key=lambda individual: original_order[individual]
        )

        objectives = [
            lambda x: x.total_distance,
            lambda x: x.difference_longest_shortest
        ]
        for objective in objectives:
            ordered_rank = sorted(rank, key=objective)

            f_min = objective(ordered_rank[0])
            f_max = objective(ordered_rank[-1])

            if f_max == f_min:
                continue

            for i in range(1, rank_size - 1):
                previous_value = objective(ordered_rank[i - 1])
                next_value = objective(ordered_rank[i + 1])
                ordered_rank[i].crowding_distance += (next_value - previous_value) / (f_max - f_min)

        total_distance_extreme.crowding_distance = float("inf")
        difference_extreme.crowding_distance = float("inf")
        return

    def print_ranks(ranks):
        for i, rank in enumerate(ranks):
            print(f"rank {i+1}: {len(rank)} individuos")
            individual : Individual
            for individual in rank:
                print(f"{individual.rank} - {individual.crowding_distance} | f1 {individual.total_distance} - f2 {individual.difference_longest_shortest}", end=" | ")
                print(f"cost per path {' - '.join(str(t) for t in individual.total_per_salesman)}")
