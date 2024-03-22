import math
import random

from tabu_data_holder import NeighbourhoodData, init_neighbour_data
from tabu_utils import tabu_calc, choose_neighbour, is_aspirational, get_path_cost, tabu_init, sample_neighborhood, \
    find_best_neighbour


def tabu(graph, start, stops, opt, start_time):
    data_holder = tabu_init(graph, opt, start, start_time, stops)

    return tabu_calc(data_holder, graph, opt, start, start_time)


def tabu_b(graph, start, stops, opt, start_time):
    current_solution = stops
    random.shuffle(current_solution)
    data_holder = tabu_init(
        graph, opt, start, start_time, stops
    )

    # MODIFICATION (2.b): Adjusting tabu tenure based on neighborhood size
    data_holder.tabu_tenure = min(
        max(1, 2 * math.floor(math.sqrt(data_holder.stops_count))), 10
    )
    data_holder.tabu_list = []

    return tabu_calc(data_holder, graph, opt, start, start_time)


def tabu_d(graph, start, stops, opt, start_time):
    data_holder = tabu_init(
        graph, opt, start, start_time, stops
    )

    for iteration in range(data_holder.max_iterations):
        if data_holder.turns_improved > data_holder.improve_thresh:
            break

        neighbourhood_data: NeighbourhoodData = init_neighbour_data()

        # getting the best_neighbour
        for i in range(data_holder.stops_count):

            # MODIFICATION (2.d): sampling
            sampled_neighbors = sample_neighborhood(data_holder.current_solution)
            for j in range(i + 1, data_holder.stops_count):
                found_neighbour = sampled_neighbors[j]

                neighbourhood_data = find_best_neighbour(
                    neighbourhood_data,
                    graph,
                    i,
                    j,
                    found_neighbour,
                    opt,
                    start,
                    start_time,
                    data_holder.tabu_list)

            data_holder.tabu_list.append((neighbourhood_data.coord_a, neighbourhood_data.coord_b))

        (neighbourhood_data, data_holder) = choose_neighbour(neighbourhood_data, data_holder)

    return (
        data_holder.best_solution,
        data_holder.best_solution_cost,
        data_holder.best_path,
        data_holder.best_arrival_time,
        data_holder.best_departure_time,
        data_holder.best_line,
    )


def tabu_c(gg, start, stops, opt, start_time):
    data_holder = tabu_init(
        gg, opt, start, start_time, stops
    )

    for iteration in range(data_holder.max_iterations):
        if data_holder.turns_improved > data_holder.improve_thresh:
            break

        neighbourhood_data = init_neighbour_data()

        # getting the best_neighbour
        for i in range(data_holder.stops_count):
            for j in range(i + 1, data_holder.stops_count):
                neighbour = data_holder.current_solution
                neighbour[i], neighbour[j] = neighbour[j], neighbour[i]  # swapping

                # calculate current cost
                (
                    neighbour_cost,
                    neighbour_path,
                    neighbour_arrival_time,
                    neighbour_departure_time,
                    neighbour_line,
                ) = get_path_cost(gg, start, neighbour, opt, start_time)

                # MODIFICATION (2.c): adding is_aspirational function
                if (i, j) not in data_holder.tabu_list or is_aspirational(neighbour_cost, data_holder.best_solution_cost):
                    print(type(neighbour_cost))
                    if neighbour_cost < neighbourhood_data.best_neighbour_cost:
                        # set new values for best_neighbour variables
                        neighbourhood_data.best_neighbour = neighbour
                        neighbourhood_data.best_neighbour_cost = neighbour_cost
                        neighbourhood_data.best_neighbour_path = neighbour_path
                        neighbourhood_data.best_neighbour_arrival_time = neighbour_arrival_time
                        neighbourhood_data.best_neighbour_departure_time = neighbour_departure_time
                        neighbourhood_data.best_neighbour_line = neighbour_line
                        neighbourhood_data.coord_a, neighbourhood_data.coord_b = i, j
            data_holder.tabu_list.append((neighbourhood_data.coord_a, neighbourhood_data.coord_b))

        (neighbourhood_data, data_holder) = choose_neighbour(neighbourhood_data, data_holder)

    return (
        data_holder.best_solution,
        data_holder.best_solution_cost,
        data_holder.best_path,
        data_holder.best_arrival_time,
        data_holder.best_departure_time,
        data_holder.best_line,
    )
