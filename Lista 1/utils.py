from datetime import timedelta, datetime
import math
from queue import PriorityQueue
from typing import Dict, List, Callable, Tuple

from connection_node import Edge


def manhattan_distance(a: Tuple[int, ...], b: Tuple[int, ...]) -> float:
    return sum(abs(x - y) for x, y in zip(a, b)) * 100


def euclidean_distance(a: Tuple[int, ...], b: Tuple[int, ...]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))) * 1000


def graph_init(graph: Dict[str, List[Edge]], start: str, start_time: timedelta) -> \
        (Dict[str, List[timedelta]],
         Dict[str, List[timedelta]],
         Dict[str, List[timedelta]],
         Dict[str, int],
         Dict[str, float],
         PriorityQueue,
         List[str]):
    previous_nodes = {
        node: None for node in graph
    }

    arrival_times = {
        node: timedelta(hours=23, minutes=59, seconds=59) for node in graph
    }

    departure_times = {
        node: timedelta(hours=23, minutes=59, seconds=59) for node in graph
    }

    lines = {
        node: 0 for node in graph
    }

    cost_so_far = {
        node: math.inf for node in graph
    }

    arrival_times[start] = start_time
    cost_so_far[start] = 0
    queue = PriorityQueue()
    queue.put((0, start, start_time))
    visited_nodes = []

    return (
        previous_nodes,
        arrival_times,
        departure_times,
        lines,
        cost_so_far,
        queue,
        visited_nodes)


def create_path(
        goal: str,
        arrival_times: Dict[str, timedelta],
        departure_times: Dict[str, timedelta],
        lines: Dict[str, int],
        prev_nodes: Dict[str, List[timedelta]]
) -> (str, timedelta, timedelta, int):
    path = []
    arrival_time = []
    departure_time = []
    curr_node = goal
    line = []

    while curr_node is not None:
        path.append(curr_node)
        arrival_time.append((datetime.min + arrival_times[curr_node]).time())
        departure_time.append((datetime.min + departure_times[curr_node]).time())
        line.append(lines[curr_node])
        curr_node = prev_nodes[curr_node]

    path.reverse()
    arrival_time.reverse()
    departure_time.reverse()
    line.reverse()

    return path, arrival_time, departure_time, line


def add_change_time(time: timedelta) -> timedelta:
    return time + timedelta(hours=0, minutes=2, seconds=0)


def check_if_will_make_it_in_time(
        edge: Edge,
        curr_line: int,
        curr_time: timedelta,
        curr_node: str,
        start: str
) -> bool:
    return ((curr_node == start and curr_time <= edge.departure_time)
            or (edge.line != curr_line and add_change_time(curr_time) <= edge.departure_time)
            or (edge.line == curr_line and curr_time == edge.departure_time))


def generic_optimisation_function(
        graph: Dict[str, List[Edge]],
        start: str,
        goal: str,
        start_time: timedelta,
        optimisation_function: Callable[[Edge, float, ], float],
        calculate_new_cost: Callable[[timedelta, timedelta], float]
) -> (int, str, timedelta, timedelta, int):
    (
        previous_nodes,
        arrival_times,
        departure_times,
        lines,
        cost_so_far,
        queue,
        visited_nodes
    ) = graph_init(graph, start, start_time)

    while not queue.empty():
        cost, curr_node, curr_time = queue.get()
        # pop the smallest item from the heap
        if curr_node not in visited_nodes:
            visited_nodes.append(curr_node)  # mark as visited

            if curr_node == goal:
                break  # done :)

            # check route to all neighbours with optimisation function
            for edge in graph[curr_node]:
                if check_if_will_make_it_in_time(edge, lines[curr_node], curr_time, curr_node, start):
                    new_cost = calculate_new_cost(edge.arrival_time, start_time)
                    # checking for a better route
                    if edge.neighbour not in visited_nodes and new_cost < cost_so_far[edge.neighbour]:
                        # set values for a neighbour
                        previous_nodes[edge.neighbour] = curr_node
                        arrival_times[edge.neighbour] = edge.arrival_time
                        departure_times[edge.neighbour] = edge.departure_time
                        lines[edge.neighbour] = edge.line
                        cost_so_far[edge.neighbour] = new_cost

                        after_optimisation = optimisation_function(
                            edge,
                            new_cost
                        )
                        queue.put((after_optimisation, edge.neighbour, edge.arrival_time))

    return cost_so_far[goal], *create_path(goal, arrival_times, departure_times, lines, previous_nodes)


def calculate_cost_simple(arrival_time: timedelta, start_time: timedelta) -> float:
    return (arrival_time - start_time).seconds / 60
