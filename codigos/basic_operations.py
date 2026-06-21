from problem import Problem

class BasicOperations:
    def __init__(self, problem : Problem):
        self.problem = problem
        pass

    def get_city_coordinates(self, city: int) -> tuple[float, float]:
        coordinates = self.problem.instance.node_coords.get(city)
        if coordinates is None:
            raise ValueError(f"Coordinates not found for city {city}")

        return float(coordinates[0]), float(coordinates[1])

    def calculate_centroid(self, route: list[int]) -> tuple[float, float]:
        if len(route) == 0:
            return self.get_city_coordinates(self.problem.first_node)
        
        route.append(self.problem.first_node) 
        coordinates = [self.get_city_coordinates(city) for city in route]
        x = sum(point[0] for point in coordinates) / len(coordinates)
        y = sum(point[1] for point in coordinates) / len(coordinates)
        route.pop()
        return x, y