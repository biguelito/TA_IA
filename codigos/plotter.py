import matplotlib.pyplot as plt

from individual import Individual
from problem import Problem
from basic_operations import BasicOperations

class Plotter:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.basic_operations = BasicOperations(self.problem)


    def __get_route_points(self, route: list[int]) -> tuple[list[float], list[float]]:
        complete_route = [self.problem.first_node] + route + [self.problem.first_node]
        x_points = []
        y_points = []

        for city in complete_route:
            x, y = self.basic_operations.get_city_coordinates(city)
            x_points.append(x)
            y_points.append(y)

        return x_points, y_points

    def __annotate_cities(self, axes):
        for city in self.problem.all_nodes:
            x, y = self.basic_operations.get_city_coordinates(city)
            axes.annotate(
                str(city),
                (x, y),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=8,
                color="black",
                zorder=6
            )

    def plot_individual(
            self,
            individual: Individual,
            show_centroids: bool = False,
            save_path: str | None = None,
            show_plot: bool = True
    ):
        if individual.salesman_paths is None or len(individual.salesman_paths) == 0:
            raise ValueError("The individual does not have decoded salesman paths to plot.")

        figure, axes = plt.subplots(figsize=(10, 8))
        cmap = plt.get_cmap("tab10")

        all_x = []
        all_y = []
        for city in self.problem.all_nodes:
            x, y = self.basic_operations.get_city_coordinates(city)
            all_x.append(x)
            all_y.append(y)

        axes.scatter(all_x, all_y, color="lightgray", s=35, zorder=1, label="Cities")

        depot_x, depot_y = self.basic_operations.get_city_coordinates(self.problem.first_node)
        axes.scatter(
            depot_x,
            depot_y,
            color="crimson",
            s=160,
            marker="*",
            edgecolors="black",
            linewidths=0.8,
            zorder=5,
            label="Depot"
        )
        self.__annotate_cities(axes)

        for index, route in enumerate(individual.salesman_paths):
            color = cmap(index % 10)
            x_points, y_points = self.__get_route_points(route)
            axes.plot(
                x_points,
                y_points,
                color=color,
                linewidth=1.8,
                zorder=2,
                label=f"Salesman {index + 1} ({individual.total_per_salesman[index]})"
            )

            if len(route) > 0:
                route_x = []
                route_y = []
                for city in route:
                    x, y = self.basic_operations.get_city_coordinates(city)
                    route_x.append(x)
                    route_y.append(y)
                axes.scatter(route_x, route_y, color=color, s=45, zorder=3)

            if show_centroids:
                centroid_x, centroid_y = self.basic_operations.calculate_centroid(route)
                axes.scatter(
                    centroid_x,
                    centroid_y,
                    color=color,
                    s=140,
                    marker="X",
                    edgecolors="black",
                    linewidths=0.8,
                    zorder=4
                )

        axes.set_title(
            f"{individual.problem.instance_name} - total distance: {individual.total_distance} - "
            f"difference: {individual.difference_longest_shortest}"
        )
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
        axes.set_aspect("equal", adjustable="box")
        axes.legend(loc="best")
        figure.tight_layout()

        if save_path is not None:
            figure.savefig(save_path, dpi=200, bbox_inches="tight")

        if show_plot:
            plt.show()
        else:
            plt.close(figure)

        return figure, axes

    def plot_pareto_front(
            self,
            individuals: list[Individual],
            save_path: str | None = None,
            show_plot: bool = True,
            max_point: tuple[int, int] | None = None,
            min_point: tuple[int, int] | None = None
    ):
        if individuals is None or len(individuals) == 0:
            raise ValueError("The list of individuals to plot cannot be empty.")

        sorted_individuals = sorted(individuals, key=lambda individual: individual.total_distance)
        x_points = [individual.total_distance for individual in sorted_individuals]
        y_points = [individual.difference_longest_shortest for individual in sorted_individuals]

        figure, axes = plt.subplots(figsize=(10, 8))
        axes.scatter(
            x_points,
            y_points,
            color="royalblue",
            s=55,
            zorder=3,
            label="Individuals"
        )
        axes.plot(
            x_points,
            y_points,
            color="royalblue",
            linewidth=1.6,
            alpha=0.8,
            zorder=2
        )

        axes.set_title(f"{individuals[0].problem.instance_name} - Pareto front - {len(sorted_individuals)} individuals")
        axes.set_xlabel("Total cost")
        axes.set_ylabel("Cost difference")
        axes.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
        axes.legend(loc="best")
        figure.tight_layout()

        if (max_point != None):
            axes.scatter(
                max_point[0],
                max_point[1],
                color="red",
                s=55,
                zorder=3,
            )
        if (min_point != None):
            axes.scatter(
                min_point[0],
                min_point[1],
                color="green",
                s=55,
                zorder=3,
            )

        if save_path is not None:
            figure.savefig(save_path, dpi=200, bbox_inches="tight")

        if show_plot:
            plt.show()
        else:
            plt.close(figure)

        return figure, axes
