from individual import Individual
from problem import Problem

import random
import copy
import math

class CommonOperators:
    def __init__(self, problem : Problem):
        self.problem = problem

    def __get_city_coordinates(self, city: int) -> tuple[float, float]:
        coordinates = self.problem.instance.node_coords.get(city)
        if coordinates is None:
            raise ValueError(f"Coordinates not found for city {city}")

        return float(coordinates[0]), float(coordinates[1])

    def __euclidean_distance(self, a: tuple[float, float], b: tuple[float, float]) -> float:
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def __path_cost(self, route: list[int]) -> float:
        salesman_path_complete = [self.problem.first_node] + route + [self.problem.first_node]
        cost = 0.0
        for point in range(len(salesman_path_complete)-1):
            cost += self.problem.instance.get_weight(salesman_path_complete[point], salesman_path_complete[point+1])
        return cost

    def __find_closest_route_by_centroid(
            self,
            base_centroid: tuple[float, float],
            candidate_indexes: list[int],
            centroids: list[tuple[float, float]]
    ) -> int:
        return min(
            candidate_indexes,
            key=lambda index: self.__euclidean_distance(base_centroid, centroids[index])
        )

    def __find_closest_city_to_centroid(self, route: list[int], centroid: tuple[float, float]) -> int:
        return min(
            route,
            key=lambda city: self.__euclidean_distance(self.__get_city_coordinates(city), centroid)
        )

    def __find_best_insertion_position(self, route: list[int], city: int) -> int:
        best_position = 0
        best_cost = None

        for position in range(len(route) + 1):
            candidate_route = route[:position] + [city] + route[position:]
            candidate_cost = self.__path_cost(candidate_route)
            if best_cost is None or candidate_cost < best_cost:
                best_cost = candidate_cost
                best_position = position

        return best_position

    def __rebuild_individual_from_routes(self, individual: Individual, routes: list[list[int]]):
        paths = []
        divisions = []
        accumulated_size = 0

        for index, route in enumerate(routes):
            paths.extend(route)
            accumulated_size += len(route)
            if index < len(routes) - 1:
                divisions.append(accumulated_size)

        individual.create_crossover(paths, divisions)
        return individual

    def __binary_tournament(self, population : list[Individual]) -> list[Individual]:
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
    
    def __rearrange_in_par(self, full_population : list[Individual]):
        return [(full_population[i], full_population[i+1]) for i in range(0, len(full_population), 2)]

    def __next_city(self, paths, city):
        position = paths.index(city)
        if position == len(paths)-1:
            return paths[0]

        return paths[position+1]

    def __crossover_operator(self, father_a : list[int], father_b : list[int]):
        city = random.sample(father_a, k=1)[0]
        child_paths = [city]
        while len(father_a) > 1:
            next_a = self.__next_city(father_a, city)
            next_b = self.__next_city(father_b, city) 
            father_a.remove(city)
            father_b.remove(city)
            distance_city_next_a = self.problem.instance.get_weight(city, next_a)
            distance_city_next_b = self.problem.instance.get_weight(city, next_b)
            if distance_city_next_a < distance_city_next_b:
                city = next_a
            else:
                city = next_b
            child_paths.append(city)
            
        return child_paths

    def __choose_division_randoms(self, a : Individual, b : Individual):
        if (random.uniform(0, 1) <= 0.5): 
            return a.divisions
        else:
            return b.divisions

    def __rationalize_complete_path(self, complete_path):
        return [city for city in complete_path if city != self.problem.first_node]

    def __crossover_first_child(self, a : Individual, b : Individual) -> Individual:
        a_paths = copy.deepcopy(a.paths)
        b_paths = copy.deepcopy(b.paths)
        
        child_paths = self.__crossover_operator(a_paths, b_paths)
        child_division = self.__choose_division_randoms(a, b)
        child = Individual(self.problem)
        child.create_crossover(child_paths, child_division)

        return child

    def __crossover_second_child(self, a : Individual, b : Individual) -> Individual:
        a_complete_paths = copy.deepcopy(a.decodified_paths)
        b_complete_paths = copy.deepcopy(b.decodified_paths)

        child_paths = self.__crossover_operator(a_complete_paths, b_complete_paths)
        child_paths = self.__rationalize_complete_path(child_paths)
        child = Individual(self.problem)
        child.create_crossover_random_divisions(child_paths)

        return child

    def calculate_centroid(self, route: list[int]) -> tuple[float, float]:
        if len(route) == 0:
            return self.__get_city_coordinates(self.problem.first_node)
        
        route.append(self.problem.first_node) 
        coordinates = [self.__get_city_coordinates(city) for city in route]
        x = sum(point[0] for point in coordinates) / len(coordinates)
        y = sum(point[1] for point in coordinates) / len(coordinates)
        route.pop()
        return x, y

    def binary_tournament_selection(self, population : list[Individual]):
        random_arragement_first_half = random.sample(population, k=len(population))
        selection_first_half = self.__binary_tournament(random_arragement_first_half)
        random_arragement_second_half = random.sample(population, k=len(population))
        selection_second_half = self.__binary_tournament(random_arragement_second_half)
        full_population = selection_first_half + selection_second_half
        return self.__rearrange_in_par(full_population)

    def crossover(self, fathers_population : list[tuple[Individual, Individual]]) -> list[Individual]:
        childs = []
        for fathers in fathers_population:
            father_a, father_b = fathers[0], fathers[1]
            child_1 = self.__crossover_first_child(father_a, father_b)
            childs.append(child_1)
            child_2 = self.__crossover_second_child(father_a, father_b)
            childs.append(child_2)

        return childs

    def rebalance_by_centroid(self, individual: Individual, mode: str) -> Individual:
        routes = copy.deepcopy(individual.salesman_paths)

        if len(routes) < 2:
            return individual

        costs = individual.total_per_salesman
        centroids = [self.calculate_centroid(route) for route in routes]

        if mode == "expand_shortest":
            destination_index = min(range(len(costs)), key=lambda index: costs[index])
            candidate_origins = [
                index for index in range(len(routes))
                if index != destination_index and len(routes[index]) > 1
            ]

            if len(candidate_origins) == 0:
                return individual

            origin_index = self.__find_closest_route_by_centroid(
                centroids[destination_index],
                candidate_origins,
                centroids
            )
            
            target_centroid = centroids[destination_index]

        elif mode == "shrink_longest":
            origin_index = max(range(len(costs)), key=lambda index: costs[index])
            if len(routes[origin_index]) <= 1:
                return individual

            candidate_destinations = [
                index for index in range(len(routes))
                if index != origin_index
            ]

            if len(candidate_destinations) == 0:
                return individual

            destination_index = self.__find_closest_route_by_centroid(
                centroids[origin_index],
                candidate_destinations,
                centroids
            )
            target_centroid = centroids[destination_index]

        else:
            return individual

        # if len(routes[origin_index]) <= 2:
        #     return individual

        city_to_move = self.__find_closest_city_to_centroid(routes[origin_index], target_centroid)
        routes[origin_index].remove(city_to_move)

        insertion_position = self.__find_best_insertion_position(routes[destination_index], city_to_move)
        routes[destination_index].insert(insertion_position, city_to_move)

        new_invidual = self.__rebuild_individual_from_routes(individual, routes)
        return new_invidual