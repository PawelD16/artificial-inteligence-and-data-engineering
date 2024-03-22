import datetime
import math
from typing import Dict, List
from connection_node import Edge
from utils import create_path, euclidean_distance, graph_init, check_if_will_make_it_in_time, \
    generic_bfs_function, calculate_cost_simple
from datetime import timedelta

T_P_MULTIPLIER = 10
P_MULTIPLIER = 100


def astar_t(graph: Dict[str, List[Edge]], start: str, goal: str, start_time: timedelta):
    # define a heuristic function
    heuristic_fn = lambda a, b: euclidean_distance(a, b)

    def astar_t_inner(edge, new_cost) -> float:
        goal_coordinates = (
            float(graph[goal][0].end_lat),  # end_stop_lat
            float(graph[goal][0].end_lon),  # end_stop_lon
        )
        neighbour_coordinates = (
            float(edge.end_lat),
            float(edge.end_lon),
        )
        # calculate distance between goal and neighbour coordinates
        return new_cost + heuristic_fn(goal_coordinates, neighbour_coordinates)

    return generic_bfs_function(graph, start, goal, start_time, astar_t_inner, calculate_cost_simple, True)


def a_star_helper(graph, start, goal, start_time, start_line, multiplier):
    # define a heuristic function
    heuristic_fn = lambda a, b: euclidean_distance(a, b)
    (
        previous_nodes,
        arrival_times,
        departure_times,
        lines,
        cost_so_far,
        queue,
        visited_nodes
    ) = graph_init(graph, start, start_time)

    lines[start] = start_line

    transfers = {node: math.inf for node in graph}
    transfers[start] = 0

    while not queue.empty():
        _, curr_node, curr_time = queue.get()
        # pop the smallest item from the heap
        if curr_node not in visited_nodes:
            visited_nodes.append(curr_node)  # mark as visited

            if curr_node == goal:
                break  # done :)

            # check route to all neighbours with optimisation function
            for edge in graph[curr_node]:
                if check_if_will_make_it_in_time(edge, lines[curr_node], curr_time, curr_node, start):
                    prev_transfers = transfers[curr_node]
                    # calculate new cost
                    new_cost = (prev_transfers * multiplier) + ((edge.arrival_time - start_time).seconds / 60)
                    if edge.line != lines[curr_node]:
                        new_cost += multiplier
                    if edge.neighbour not in visited_nodes and new_cost < cost_so_far[edge.neighbour]:
                        # update variables
                        previous_nodes[edge.neighbour] = curr_node
                        arrival_times[edge.neighbour] = edge.arrival_time
                        departure_times[edge.neighbour] = edge.departure_time
                        lines[edge.neighbour] = edge.line
                        cost_so_far[edge.neighbour] = new_cost
                        transfers[edge.neighbour] = prev_transfers

                        if edge.line != lines[curr_node]:
                            transfers[edge.neighbour] += 1

                        goal_coordinates = (
                            float(graph[goal][0].end_lat),  # end_stop_lat
                            float(graph[goal][0].end_lon),  # end_stop_lon
                        )
                        neighbour_coordinates = (
                            float(edge.end_lat),
                            float(edge.end_lon),
                        )
                        # calculate distance between goal and neighbour coordinates
                        priority = new_cost + heuristic_fn(
                            goal_coordinates, neighbour_coordinates
                        )
                        queue.put((priority, edge.neighbour, edge.arrival_time))

    return goal, arrival_times, departure_times, lines, previous_nodes, cost_so_far


def astar_p(graph: Dict[str, List[Edge]], start, goal, start_time):
    return astar_generic_helper(graph, goal, start, start_time, P_MULTIPLIER)


def astar_t_p(graph: Dict[str, List[Edge]], start, goal, start_time):
    return astar_generic_helper(graph, goal, start, start_time, T_P_MULTIPLIER)


def astar_generic_helper(graph: Dict[str, List[Edge]], goal, start, start_time, multiplier):
    available_lines = []
    for edge in graph[start]:
        if edge.line not in available_lines:
            available_lines.append(edge.line)
    # initialize variables
    final_cost = math.inf
    final_arrival_times = {}
    final_departure_times = {}
    final_lines = {}
    final_prev_nodes = {}
    for line in available_lines:
        (
            goal,
            arrival_times,
            departure_times,
            lines,
            prev_nodes,
            cost_so_far,
        ) = a_star_helper(graph, start, goal, start_time, line, multiplier)

        if final_cost > cost_so_far[goal]:
            # set new values for final variables
            final_cost = cost_so_far[goal]
            final_arrival_times = arrival_times
            final_departure_times = departure_times
            final_lines = lines
            final_prev_nodes = prev_nodes
    path, arrival_time, departure_time, line = create_path(
        goal, final_arrival_times, final_departure_times, final_lines, final_prev_nodes
    )
    return cost_so_far[goal], path, arrival_time, departure_time, line


