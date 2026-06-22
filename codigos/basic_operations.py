from problem import Problem
# from numpy import np
import math

class BasicOperations:
    def __init__(self, problem : Problem):
        self.problem = problem
        pass

    def __pareto_points(self, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        return sorted(set(points), key=lambda point: (point[0], point[1]))

    def get_city_coordinates(self, city: int) -> tuple[float, float]:
        coordinates = self.problem.instance.node_coords.get(city)
        if coordinates is None:
            raise ValueError(f"Coordinates not found for city {city}")

        return float(coordinates[0]), float(coordinates[1])

    def __calculate_centroid(self, coordinates : list[tuple[int, int]]):
        x = sum(point[0] for point in coordinates) / len(coordinates)
        y = sum(point[1] for point in coordinates) / len(coordinates)
        return x, y

    def calculate_centroid_by_cities(self, route: list[int]) -> tuple[float, float]:
        if len(route) == 0:
            return self.get_city_coordinates(self.problem.first_node)
        
        route.append(self.problem.first_node) 
        coordinates = [self.get_city_coordinates(city) for city in route]
        x, y = self.__calculate_centroid(coordinates)
        route.pop()
        return x, y
    
    def calculate_centroid_by_points(self, points: list[tuple[int, int]]):
        return self.__calculate_centroid(points)
    
    def calculate_spacing(self, points: list[tuple[int, int]]):
        points = self.__pareto_points(points)
        n = len(points)

        if n < 2:
            return 0.0

        nearest_distances = []
        for i, p in enumerate(points):
            distances = [math.dist(p, q) for j, q in enumerate(points) if i != j]
            nearest_distances.append(min(distances))

        mean_d = sum(nearest_distances) / n
        return math.sqrt(sum((d - mean_d) ** 2 for d in nearest_distances) / (n - 1))

    def calculate_spreading(self, points: list[tuple[int, int]]):
        points = self.__pareto_points(points)
        n = len(points)
        if n < 2:
            return 0.0

        max_point = self.problem.get_nadir_point()
        min_point = self.problem.get_min_point()
        left_theoretical_extreme = (min_point[0], max_point[1])
        right_theoretical_extreme = (max_point[0], min_point[1])

        consecutive_distances = [
            math.dist(points[i], points[i + 1])
            for i in range(n - 1)
        ]
        mean_distance = sum(consecutive_distances) / (n - 1)

        distance_first_extreme = math.dist(points[0], left_theoretical_extreme)
        distance_last_extreme = math.dist(points[-1], right_theoretical_extreme)

        denominator = distance_first_extreme + distance_last_extreme + ((n - 1) * mean_distance)
        if denominator == 0:
            return 0.0

        numerator = (
            distance_first_extreme
            + distance_last_extreme
            + sum(abs(distance - mean_distance) for distance in consecutive_distances)
        )
        return numerator / denominator
