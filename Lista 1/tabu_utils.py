import math
from datetime import timedelta
from random import shuffle, sample

from a_star import astar_p, astar_t
from dijkstra import dijkstra_t
from tabu_data_holder import TabuDataHolder, NeighbourhoodData, init_neighbour_data


def tabu_init(graph, opt, start, start_time, stops) -> TabuDataHolder:
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
    return TabuDataHolder(
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
    )


def get_path_cost(graph, start, stops, opt, start_time):
    curr_time = start_time
    curr_stop = start
    final_cost = 0
    final_path = [start]
    final_arrival_time = [""]
    final_departure_time = [""]
    final_line = [""]

    for stop in stops:
        if opt == "t":
            cost, path, arrival_time, departure_time, line = astar_t(graph, curr_stop, stop, curr_time)
        elif opt == "p":
            cost, path, arrival_time, departure_time, line = astar_p(graph, curr_stop, stop, curr_time)

        if opt == "t" or opt == "p":
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
        graph, curr_stop, start, curr_time
    )

    # update variables by adding calculated values
    final_cost += cost
    final_path = final_path + path[1:]
    final_arrival_time = final_arrival_time + arrival_time[1:]
    final_departure_time = final_departure_time + departure_time[1:]
    final_line = final_line + line[1:]
    return final_cost, final_path, final_arrival_time, final_departure_time, final_line


def is_aspirational(cost, best_solution_cost):
    return cost < 0.8 * best_solution_cost


def sample_neighborhood(current_solution):
    if len(current_solution) < 2:
        return current_solution

    sampled_neighbors = []
    for _ in range(len(current_solution)):
        neighbor = current_solution[:]
        i, j = sample(range(len(current_solution)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        sampled_neighbors.append(neighbor)
    return sampled_neighbors


def tabu_calc(data_holder, graph, opt, start, start_time):
    for iteration in range(data_holder.max_iterations):
        if data_holder.turns_improved > data_holder.improve_thresh:
            break

        neighbourhood_data = init_neighbour_data()

        # getting the best_neighbour
        for i in range(data_holder.stops_count):
            for j in range(i + 1, data_holder.stops_count):
                neighbour = data_holder.current_solution
                neighbour[i], neighbour[j] = neighbour[j], neighbour[i]  # swapping

                neighbourhood_data = find_best_neighbour(
                    neighbourhood_data,
                    graph,
                    i,
                    j,
                    neighbour,
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


def choose_neighbour(
        neighbourhood_data: NeighbourhoodData,
        tabu_data: TabuDataHolder
) -> (NeighbourhoodData, TabuDataHolder):
    if neighbourhood_data.best_neighbour is not None:
        tabu_data.current_solution = neighbourhood_data.best_neighbour
        tabu_data.tabu_list.append((neighbourhood_data.coord_a, neighbourhood_data.coord_b))

        if len(tabu_data.tabu_list) > tabu_data.tabu_tenure:
            tabu_data.tabu_list.pop(0)
        if neighbourhood_data.best_neighbour_cost < tabu_data.best_solution_cost:
            # set new values for best_variables
            tabu_data.best_solution = neighbourhood_data.best_neighbour
            tabu_data.best_solution_cost = neighbourhood_data.best_neighbour_cost
            tabu_data.best_path = neighbourhood_data.best_neighbour_path
            tabu_data.best_arrival_time = neighbourhood_data.best_neighbour_arrival_time
            tabu_data.best_departure_time = neighbourhood_data.best_neighbour_departure_time
            tabu_data.best_line = neighbourhood_data.best_neighbour_line
            # reset turns counter
            tabu_data.turns_improved = 0
        else:
            tabu_data.turns_improved = tabu_data.turns_improved + 1
    return neighbourhood_data, tabu_data


def find_best_neighbour(
        neighbourhood_data: NeighbourhoodData,
        graph,
        i,
        j,
        neighbour,
        opt,
        start,
        start_time,
        tabu_list) -> NeighbourhoodData:
    (
        neighbour_cost,
        neighbour_path,
        neighbour_arrival_time,
        neighbour_departure_time,
        neighbour_line,
    ) = get_path_cost(graph, start, neighbour, opt, start_time)
    if (i, j) not in tabu_list:
        if neighbour_cost < neighbourhood_data.best_neighbour_cost:
            # set new values for best_neighbour variables
            neighbourhood_data.best_neighbour = neighbour
            neighbourhood_data.best_neighbour_cost = neighbour_cost
            neighbourhood_data.best_neighbour_path = neighbour_path
            neighbourhood_data.best_neighbour_arrival_time = neighbour_arrival_time
            neighbourhood_data.best_neighbour_departure_time = neighbour_departure_time
            neighbourhood_data.best_neighbour_line = neighbour_line
            neighbourhood_data.coord_a, neighbourhood_data.coord_b = i, j

    return neighbourhood_data
