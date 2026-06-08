from individual import Individual

class NSGA2:
    def __init__(self):
        pass

    def a_dominates_b(self, a : Individual, b : Individual):
        better_or_equal_every = (
            a.total_distance <= b.total_distance 
            and a.difference_longest_shortest <= b.difference_longest_shortest
        )

        better_least_one = (
            a.total_distance < b.total_distance
            or a.difference_longest_shortest < b.difference_longest_shortest
        )

        return better_or_equal_every and better_least_one
    
    def fast_non_dominated_sort(self, population : list[Individual]):
        fronts = [[]]
        for a in population:
            a.dominated_solutions = []
            a.domination_count = 0

            for b in population:
                if a is b:
                    continue

                if self.a_dominates_b(a, b):
                    a.dominated_solutions.append(b)

                elif self.a_dominates_b(b, a):
                    a.domination_count += 1

            if a.domination_count == 0:
                a.rank = 1
                fronts[0].append(a)

        i = 0
        while len(fronts[i]) > 0:
            next_front = []
            for a in fronts[i]:
                for b in a.dominated_solutions:
                    b.domination_count -= 1

                    if b.domination_count == 0:
                        b.rank = i + 2
                        next_front.append(b)
                        
            i += 1
            fronts.append(next_front)

        fronts.pop()
        return fronts