import math
from datetime import timedelta
from random import shuffle, sample

from a_star import astar_p, astar_t
from dijkstra import dijkstra_t


def tabu_init(graph, opt, start, start_time, stops):
    stops_count = len(stops)
    current_solution = stops
    shuffle(current_solution)
    best_solution = current_solution
    # calculate cost
    (
        best_solution_cost,
        best_path,
        best_arrival_time,
        best_departure_time,
        best_line,
    ) = get_path_cost(graph, start, best_solution, opt, start_time)
    max_iterations = math.ceil(1.1 * (stops_count ** 2))
    turns_improved = 0
    improve_thresh = 2 * math.floor(math.sqrt(max_iterations))
    tabu_tenure = stops_count
    tabu_list = []
    return (
        best_arrival_time,
        best_departure_time,
        best_line,
        best_path,
        best_solution,
        best_solution_cost,
        current_solution,
        improve_thresh,
        max_iterations,
        stops_count,
        tabu_list,
        tabu_tenure,
        turns_improved)


def get_path_cost(gg, start, stops, opt, start_time):
    # initialize variables
    curr_time = start_time
    curr_stop = start
    final_cost = 0
    final_path = [start]
    final_arrival_time = [""]
    final_departure_time = [""]
    final_line = [""]

    for stop in stops:
        if opt == "t":
            cost, path, arrival_time, departure_time, line = astar_t(gg, curr_stop, stop, curr_time)
        elif opt == "p":
            cost, path, arrival_time, departure_time, line = astar_p(gg, curr_stop, stop, curr_time)

        # update variables by adding calculated values
        final_cost += cost
        final_path = final_path + path[1:]
        final_arrival_time = final_arrival_time + arrival_time[1:]
        final_departure_time = final_departure_time + departure_time[1:]
        final_line = final_line + line[1:]

        curr_stop = stop
        curr_time = timedelta(
            hours=arrival_time[len(path) - 1].hour,
            minutes=arrival_time[len(path) - 1].minute,
            seconds=arrival_time[len(path) - 1].second,
        )

    # run dijkstra
    cost, path, arrival_time, departure_time, line = dijkstra_t(
        gg, curr_stop, start, curr_time
    )

    # update variables by adding calculated values
    final_cost += cost
    final_path = final_path + path[1:]
    final_arrival_time = final_arrival_time + arrival_time[1:]
    final_departure_time = final_departure_time + departure_time[1:]
    final_line = final_line + line[1:]
    return final_cost, final_path, final_arrival_time, final_departure_time, final_line


def is_aspirational(cost, best_solution_cost):
    threshold = 0.8 * best_solution_cost
    return cost < threshold


def sample_neighborhood(current_solution):
    sampled_neighbors = []
    for _ in range(len(current_solution)):
        neighbor = current_solution[:]
        i, j = sample(range(len(current_solution)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        sampled_neighbors.append(neighbor)
    return sampled_neighbors


def tabu_calc(
        best_arrival_time,
        best_departure_time,
        best_line,
        best_path,
        best_solution,
        best_solution_cost,
        current_solution,
        gg,
        improve_thresh,
        max_iterations,
        opt,
        start,
        start_time,
        stops_count,
        tabu_list,
        tabu_tenure,
        turns_improved
):
    for iteration in range(max_iterations):
        if turns_improved > improve_thresh:
            break

        # initialize variables
        best_neighbour = None
        best_neighbour_cost = float("inf")
        best_neighbour_path = []
        best_neighbour_arrival_time = []
        best_neighbour_departure_time = []
        best_neighbour_line = []
        coord_a, coord_b = 0, 0

        # getting the best_neighbour
        for i in range(stops_count):
            for j in range(i + 1, stops_count):
                neighbour = current_solution
                neighbour[i], neighbour[j] = neighbour[j], neighbour[i]  # swapping

                (
                    best_neighbour,
                    best_neighbour_arrival_time,
                    best_neighbour_cost,
                    best_neighbour_departure_time,
                    best_neighbour_line,
                    best_neighbour_path,
                    coord_a, coord_b
                ) = find_best_neighbour(
                    best_neighbour,
                    best_neighbour_arrival_time,
                    best_neighbour_cost,
                    best_neighbour_departure_time,
                    best_neighbour_line,
                    best_neighbour_path,
                    coord_a,
                    coord_b,
                    gg,
                    i,
                    j,
                    neighbour,
                    opt,
                    start,
                    start_time,
                    tabu_list)
            tabu_list.append((coord_a, coord_b))

        (
            best_arrival_time,
            best_departure_time,
            best_line,
            best_path,
            best_solution,
            best_solution_cost,
            current_solution,
            turns_improved
        ) = choose_neighbour(
            best_arrival_time,
            best_departure_time,
            best_line,
            best_neighbour,
            best_neighbour_arrival_time,
            best_neighbour_cost,
            best_neighbour_departure_time,
            best_neighbour_line,
            best_neighbour_path,
            best_path,
            best_solution,
            best_solution_cost,
            coord_a,
            coord_b,
            current_solution,
            tabu_list,
            tabu_tenure,
            turns_improved
        )
    return (
        best_solution,
        best_solution_cost,
        best_path,
        best_arrival_time,
        best_departure_time,
        best_line,
    )


def choose_neighbour(
        best_arrival_time,
        best_departure_time,
        best_line,
        best_neighbour,
        best_neighbour_arrival_time,
        best_neighbour_cost,
        best_neighbour_departure_time,
        best_neighbour_line,
        best_neighbour_path,
        best_path,
        best_solution,
        best_solution_cost,
        coord_a,
        coord_b,
        current_solution,
        tabu_list,
        tabu_tenure,
        turns_improved
):
    if best_neighbour is not None:
        current_solution = best_neighbour
        tabu_list.append((coord_a, coord_b))

        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)
        if best_neighbour_cost < best_solution_cost:
            # set new values for best_variables
            best_solution = best_neighbour
            best_solution_cost = best_neighbour_cost
            best_path = best_neighbour_path
            best_arrival_time = best_neighbour_arrival_time
            best_departure_time = best_neighbour_departure_time
            best_line = best_neighbour_line
            # reset turns counter
            turns_improved = 0
        else:
            turns_improved = turns_improved + 1
    return (
        best_arrival_time,
        best_departure_time,
        best_line, best_path,
        best_solution,
        best_solution_cost,
        current_solution,
        turns_improved
    )


def find_best_neighbour(
        best_neighbour,
        best_neighbour_arrival_time,
        best_neighbour_cost,
        best_neighbour_departure_time,
        best_neighbour_line,
        best_neighbour_path,
        coord_a,
        coord_b,
        gg,
        i,
        j,
        neighbour,
        opt,
        start,
        start_time,
        tabu_list):
    (
        neighbour_cost,
        neighbour_path,
        neighbour_arrival_time,
        neighbour_departure_time,
        neighbour_line,
    ) = get_path_cost(gg, start, neighbour, opt, start_time)
    if (i, j) not in tabu_list:

        if neighbour_cost < best_neighbour_cost:
            # set new values for best_neighbour variables
            best_neighbour = neighbour
            best_neighbour_cost = neighbour_cost
            best_neighbour_path = neighbour_path
            best_neighbour_arrival_time = neighbour_arrival_time
            best_neighbour_departure_time = neighbour_departure_time
            best_neighbour_line = neighbour_line
            coord_a, coord_b = i, j
    return (
        best_neighbour,
        best_neighbour_arrival_time,
        best_neighbour_cost,
        best_neighbour_departure_time,
        best_neighbour_line,
        best_neighbour_path,
        coord_a,
        coord_b
    )
