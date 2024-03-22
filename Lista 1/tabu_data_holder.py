import math
from datetime import timedelta
from typing import List


class TabuDataHolder:
    def __init__(
            self,
            best_arrival_time: timedelta,
            best_departure_time: timedelta,
            best_line: int,
            best_path: List[str],
            best_solution: List[str],
            best_solution_cost: float,
            current_solution: List[str],
            improve_thresh: int,
            max_iterations: int,
            stops_count: int,
            tabu_list: List[tuple],
            tabu_tenure: float,
            turns_improved: int
    ):
        self.best_arrival_time = best_arrival_time
        self.best_departure_time = best_departure_time
        self.best_line = best_line
        self.best_path = best_path
        self.best_solution = best_solution
        self.best_solution_cost = best_solution_cost
        self.current_solution = current_solution
        self.improve_thresh = improve_thresh
        self.max_iterations = max_iterations
        self.stops_count = stops_count
        self.tabu_list = tabu_list
        self.tabu_tenure = tabu_tenure
        self.turns_improved = turns_improved


class NeighbourhoodData:
    def __init__(
            self,
            best_neighbour,
            best_neighbour_arrival_time: List[timedelta],
            best_neighbour_cost: float,
            best_neighbour_departure_time: List[timedelta],
            best_neighbour_line: List[int],
            best_neighbour_path: List[str],
            coord_a: int,
            coord_b: int
    ):
        self.best_neighbour = best_neighbour
        self.best_neighbour_arrival_time = best_neighbour_arrival_time
        self.best_neighbour_cost = best_neighbour_cost
        self.best_neighbour_departure_time = best_neighbour_departure_time
        self.best_neighbour_line = best_neighbour_line
        self.best_neighbour_path = best_neighbour_path
        self.coord_a = coord_a
        self.coord_b = coord_b


def init_neighbour_data() -> NeighbourhoodData:
    best_neighbour = None
    best_neighbour_cost = math.inf
    best_neighbour_path = []
    best_neighbour_arrival_time = []
    best_neighbour_departure_time = []
    best_neighbour_line = []
    coord_a, coord_b = 0, 0
    return NeighbourhoodData(
        best_neighbour,
        best_neighbour_arrival_time,
        best_neighbour_cost,
        best_neighbour_departure_time,
        best_neighbour_line,
        best_neighbour_path,
        coord_a,
        coord_b
    )
