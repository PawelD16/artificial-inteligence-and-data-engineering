from a_star import *
from dijkstra import dijkstra_t
import time
import datetime
from tabu import tabu, tabu_b, tabu_c, tabu_d
from graph_parser import get_graph_dict
from utils import manhattan_distance, euclidean_distance, print_path


def run_dijkstra(graph, start, finish, start_time):
    print("_________________________ Dijkstra _________________________")
    print_path(*dijkstra_t(graph, start, finish, start_time))


def run_astar(graph, start, finish, opt, departure_time,
              heuristic_fn: Callable[[tuple[float, ...], tuple[float, ...]], float]):
    if opt == "all":
        run_astar(graph, start, finish, "t", departure_time, heuristic_fn)
        run_astar(graph, start, finish, "p", departure_time, heuristic_fn)
        run_astar(graph, start, finish, "both", departure_time, heuristic_fn)
    elif opt == "t":
        print("\n_________________________ A* - time _________________________")
        print_path(*astar_t(graph, start, finish, departure_time, heuristic_fn))
    elif opt == "p":
        print("\n_________________________ A* - transfers _________________________")
        print_path(*astar_p(graph, start, finish, departure_time, heuristic_fn))
    else:
        print("\n_________________________ A* - time & transfers _________________________")
        print_path(*astar_t_p(graph, start, finish, departure_time, heuristic_fn))


def run_tabu(graph, start, stops, opt, departure_time, tabu_function,
             heuristic_fn: Callable[[tuple[float, ...], tuple[float, ...]], float]):
    if opt == "all":
        run_tabu(graph, start, stops, "t", departure_time, tabu_function, heuristic_fn)
        run_tabu(graph, start, stops, "p", departure_time, tabu_function, heuristic_fn)
    else:
        if opt == "t":
            print(f"\n---------- TABU SEARCH - time - {tabu_function.__name__} ------------------------")
        elif opt == "p":
            print(f"\n---------- TABU SEARCH - transfers - {tabu_function.__name__} ------------------------")

        exe_start_time = time.time()
        solution, cost, path, arrival_time, departure_time, line = tabu_function(
            graph, start, stops, opt, departure_time, heuristic_fn
        )
        exe_end_time = time.time()
        print(f"stop count = {len(stops)} : ", exe_end_time - exe_start_time, "\n")
        print_path(cost, path, arrival_time, departure_time, line)


def run_user_queries(graph, heuristic_fn: Callable[[tuple[float, ...], tuple[float, ...]], float]):
    start = input("Przystanek początkowy A: ")
    goal = input("Przystanek końcowy B: ")
    opt = input("Kryterium optymalizacyjne (t - czas, p - przesiadki): ")
    arrival_time = input("Czas pojawienia się na przystanku A (hh:mm): ").split(":")
    hour, minutes = [int(item) for item in arrival_time]

    run_dijkstra(
        graph, start, goal, datetime.timedelta(hours=hour, minutes=minutes, seconds=0)
    )

    run_astar(
        graph, start, goal, opt, datetime.timedelta(hours=hour, minutes=minutes, seconds=0), heuristic_fn
    )

    start = input("Przystanek początkowy A: ")
    stops = input("Przystanek do odwiedzenia: ")
    opt = input("Kryterium optymalizacyjne (t - czas, p - przesiadki, all - oba): ")
    arrival_time = input("Czas pojawienia się na przystanku A (hh:mm): ").split(":")
    hour, minutes = [int(item) for item in arrival_time]

    run_tabu(graph, start, stops, opt, datetime.timedelta(hours=hour, minutes=minutes, seconds=0), tabu, heuristic_fn)


def run_automatic_queries(graph, heuristic_fn: Callable[[tuple[float, ...], tuple[float, ...]], float]):
    run_dijkstra(
        graph,
        "Katedra",
        "Niedźwiedzia",
        datetime.timedelta(hours=12, minutes=30, seconds=0),
    )

    run_astar(
        graph,
        "Katedra",
        "Niedźwiedzia",
        "all",
        datetime.timedelta(hours=12, minutes=30, seconds=0),
        heuristic_fn
    )

    run_tabu(
        graph,
        "Katedra",
        ["Kościuszki", "Rynek", "Opera"],
        "all",
        datetime.timedelta(hours=12, minutes=30, seconds=0),
        tabu,
        heuristic_fn
    )


def time_comparison(graph, heuristic_fn: Callable[[tuple[float, ...], tuple[float, ...]], float]):
    print("MAŁY DYSTANS:")
    start = "PL. GRUNWALDZKI"
    stop = "GALERIA DOMINIKAŃSKA"
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    run_optimization_algorithms(graph, start, stop, start_time, heuristic_fn)

    print("\n\n\n\nŚREDNI DYSTANS:")
    start = "Katedra"
    stop = "Niedźwiedzia"
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    run_optimization_algorithms(graph, start, stop, start_time, heuristic_fn)

    print("\n\n\n\nDUŻY DYSTANS:")
    start = "KROMERA"
    stop = "Parafialna"
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    run_optimization_algorithms(graph, start, stop, start_time, heuristic_fn)


def run_optimization_algorithms(graph, start, stop, start_time, heuristic_fn):
    exe_start_time = time.time()
    run_dijkstra(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("Dijkstra: ", exe_end_time - exe_start_time)

    # running each by itself like this because of measuring time
    exe_start_time = time.time()
    run_astar(graph, start, stop, "p", start_time, heuristic_fn)
    exe_end_time = time.time()
    print("A* - time: ", exe_end_time - exe_start_time)

    exe_start_time = time.time()
    run_astar(graph, start, stop, "t", start_time, heuristic_fn)
    exe_end_time = time.time()
    print("A* - transfers: ", exe_end_time - exe_start_time, "\n")

    exe_start_time = time.time()
    run_astar(graph, start, stop, "pt", start_time, heuristic_fn)
    exe_end_time = time.time()
    print("A* - time & transfers: ", exe_end_time - exe_start_time, "\n")


def tabu_time_comparison(
        graph,
        opt,
        tabu_function,
        heuristic_fn: Callable[[tuple[float, ...], tuple[float, ...]], float]
):
    start = "KROMERA"
    stops = ["GALERIA DOMINIKAŃSKA"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    run_tabu(graph, start, stops, opt, start_time, tabu_function, heuristic_fn)

    start = "KROMERA"
    stops = ["PL. GRUNWALDZKI", "Rynek"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    run_tabu(graph, start, stops, opt, start_time, tabu_function, heuristic_fn)

    start = "KROMERA"
    stops = ["Katedra", "GALERIA DOMINIKAŃSKA", "Niedźwiedzia"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    run_tabu(graph, start, stops, opt, start_time, tabu_function, heuristic_fn)


def run_all_tabu(graph, heuristic_fn: Callable[[tuple[float, ...], tuple[float, ...]], float]):
    tabu_time_comparison(graph, "all", tabu, heuristic_fn)
    tabu_time_comparison(graph, "all", tabu_b, heuristic_fn)
    tabu_time_comparison(graph, "all", tabu_c, heuristic_fn)
    tabu_time_comparison(graph, "all", tabu_d, heuristic_fn)


if __name__ == "__main__":
    the_graph = get_graph_dict()
    print("__________________ EUCLIDEAN DISTANCE __________________")
    time_comparison(the_graph, euclidean_distance)

    print("\n\n__________________ MANHATTAN DISTANCE __________________")
    time_comparison(the_graph, manhattan_distance)
