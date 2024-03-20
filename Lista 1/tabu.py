import math
import random
from tabu_utils import tabu_calc, choose_neighbour, is_aspirational, get_path_cost, tabu_init, sample_neighborhood, \
    find_best_neighbour


def tabu(gg, start, stops, opt, start_time):
    (
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
        turns_improved
    ) = tabu_init(
        gg, opt, start, start_time, stops
    )

    # MODIFICATION (2.b): Adjusting tabu tenure based on neighborhood size
    # tabu_tenure = min(max(1, 2 * math.floor(math.sqrt(stops_count))), 10)  # Setting min and max tabu tenure
    # tabu_list = []

    return tabu_calc(
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
        turns_improved)


def tabu_b(gg, start, stops, opt, start_time):
    current_solution = stops
    random.shuffle(current_solution)
    (
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
        turns_improved
    ) = tabu_init(
        gg, opt, start, start_time, stops
    )

    # MODIFICATION (2.b): Adjusting tabu tenure based on neighborhood size
    tabu_tenure = min(
        max(1, 2 * math.floor(math.sqrt(stops_count))), 10
    )  # Setting min and max tabu tenure
    tabu_list = []

    return tabu_calc(
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
        turns_improved)


def tabu_d(gg, start, stops, opt, start_time):
    (
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
        turns_improved
    ) = tabu_init(
        gg, opt, start, start_time, stops
    )

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

            # MODIFICATION (2.d): sampling
            sampled_neighbors = sample_neighborhood(current_solution)
            for j in range(i + 1, stops_count):
                neighbour = sampled_neighbors[j]

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


def tabu_c(gg, start, stops, opt, start_time):
    (
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
        turns_improved
    ) = tabu_init(
        gg, opt, start, start_time, stops
    )

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

                # calculate current cose
                (
                    neighbour_cost,
                    neighbour_path,
                    neighbour_arrival_time,
                    neighbour_departure_time,
                    neighbour_line,
                ) = get_path_cost(gg, start, neighbour, opt, start_time)

                # MODIFICATION (2.c): adding is_aspirational function
                if (i, j) not in tabu_list or is_aspirational(neighbour_cost, best_solution_cost):
                    if neighbour_cost < best_neighbour_cost:
                        # set new values for best_neighbour variables
                        best_neighbour = neighbour
                        best_neighbour_cost = neighbour_cost
                        best_neighbour_path = neighbour_path
                        best_neighbour_arrival_time = neighbour_arrival_time
                        best_neighbour_departure_time = neighbour_departure_time
                        best_neighbour_line = neighbour_line
                        coord_a, coord_b = i, j
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
