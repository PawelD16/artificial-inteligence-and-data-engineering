from a_star import *
from dijkstra import dijkstra_t
from printing import print_path
import time
import datetime
from tabu import tabu, tabu_b, tabu_c, tabu_d
from graph_parser import get_graph_dict


def run_dijkstra(graph, start, finish, start_time):
    print("_________________________ Dijkstra _________________________")
    print_path(*dijkstra_t(graph, start, finish, start_time))


def run_astar(graph, start, finish, opt, departure_time):
    if opt == "all":
        run_astar(graph, start, finish, "t", departure_time)
        run_astar(graph, start, finish, "p", departure_time)
        run_astar(graph, start, finish, "both", departure_time)
    elif opt == "t":
        print("\n_________________________ A* - time _________________________")
        print_path(*astar_t(graph, start, finish, departure_time))
    elif opt == "p":
        print("\n_________________________ A* - transfers _________________________")
        print_path(*astar_p(graph, start, finish, departure_time))
    else:
        print("\n_________________________ A* - time & transfers _________________________")
        print_path(*astar_t_p(graph, start, finish, departure_time))


def run_tabu(graph, start, stops, opt, departure_time, tabu_function):
    if opt == "all":
        run_tabu(graph, start, stops, "t", departure_time, tabu_function)
        run_tabu(graph, start, stops, "p", departure_time, tabu_function)
    else:
        if opt == "t":
            print(f"\n---------- TABU SEARCH - time - {tabu_function.__name__} ------------------------")
        elif opt == "p":
            print(f"\n---------- TABU SEARCH - transfers - {tabu_function.__name__} ------------------------")

        exe_start_time = time.time()
        solution, cost, path, arrival_time, departure_time, line = tabu_function(
            graph, start, stops, opt, departure_time
        )
        exe_end_time = time.time()
        print(f"stop count = {len(stops)} : ", exe_end_time - exe_start_time, "\n")
        print_path(cost, path, arrival_time, departure_time, line)


def run_user_queries(graph):
    start = input("Przystanek początkowy A: ")
    goal = input("Przystanek końcowy B: ")
    opt = input("Kryterium optymalizacyjne (t - czas, p - przesiadki): ")
    arrival_time = input("Czas pojawienia się na przystanku A (hh:mm): ").split(":")
    hour, minutes = [int(item) for item in arrival_time]
    run_dijkstra(
        graph, start, goal, datetime.timedelta(hours=hour, minutes=minutes, seconds=0)
    )
    run_astar(
        graph, start, goal, opt, datetime.timedelta(hours=hour, minutes=minutes, seconds=0)
    )

    start = input("Przystanek początkowy A: ")
    stops = input("Przystanek do odwiedzenia: ")
    opt = input("Kryterium optymalizacyjne (t - czas, p - przesiadki): ")
    arrival_time = input("Czas pojawienia się na przystanku A (hh:mm): ").split(":")
    hour, minutes = [int(item) for item in arrival_time]
    tabu(
        graph, start, goal, opt, datetime.timedelta(hours=hour, minutes=minutes, seconds=0)
    )


def run_automatic_queries(graph):
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
    )
    run_tabu(
        graph,
        "Katedra",
        ["Kościuszki", "Rynek", "Opera"],
        "all",
        datetime.timedelta(hours=12, minutes=30, seconds=0),
        tabu
    )


def time_comparison(graph):
    # little distance
    start = "PL. GRUNWALDZKI"
    stop = "GALERIA DOMINIKAŃSKA"
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)

    exe_start_time = time.time()
    dijkstra_t(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("Dijkstra: ", exe_end_time - exe_start_time)

    exe_start_time = time.time()
    astar_t(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("A* - time: ", exe_end_time - exe_start_time)

    exe_start_time = time.time()
    astar_p(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("A* - transfers: ", exe_end_time - exe_start_time, "\n")

    # medium distance
    start = "Katedra"
    stop = "Niedźwiedzia"
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)

    exe_start_time = time.time()
    dijkstra_t(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("Dijkstra: ", exe_end_time - exe_start_time)

    exe_start_time = time.time()
    astar_t(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("A* - time: ", exe_end_time - exe_start_time)

    exe_start_time = time.time()
    astar_p(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("A* - transfers: ", exe_end_time - exe_start_time, "\n")

    # big distance
    start = "KROMERA"
    stop = "Parafialna"
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)

    exe_start_time = time.time()
    dijkstra_t(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("Dijkstra: ", exe_end_time - exe_start_time)

    exe_start_time = time.time()
    astar_t(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("A* - time: ", exe_end_time - exe_start_time)

    exe_start_time = time.time()
    astar_p(graph, start, stop, start_time)
    exe_end_time = time.time()
    print("A* - transfers: ", exe_end_time - exe_start_time, "\n")

    # tabu
    start = "KROMERA"
    stops = ["GALERIA DOMINIKAŃSKA"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    exe_start_time = time.time()
    tabu(graph, start, stops, "t", start_time)
    exe_end_time = time.time()
    print("1 stop: ", exe_end_time - exe_start_time, "\n")

    start = "KROMERA"
    stops = ["PL. GRUNWALDZKI", "Rynek"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    exe_start_time = time.time()
    tabu(graph, start, stops, "t", start_time)
    exe_end_time = time.time()
    print("2 stops: ", exe_end_time - exe_start_time, "\n")

    start = "KROMERA"
    stops = ["Katedra", "GALERIA DOMINIKAŃSKA", "Niedźwiedzia"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    exe_start_time = time.time()
    tabu(graph, start, stops, "t", start_time)
    exe_end_time = time.time()
    print("3 stops: ", exe_end_time - exe_start_time, "\n")

    start = "KROMERA"
    stops = ["Katedra", "GALERIA DOMINIKAŃSKA", "Niedźwiedzia", "Przybyszewskiego"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    exe_start_time = time.time()
    tabu(graph, start, stops, "t", start_time)
    exe_end_time = time.time()
    print("4 stops: ", exe_end_time - exe_start_time, "\n")

    start = "KROMERA"
    stops = [
        "Katedra",
        "GALERIA DOMINIKAŃSKA",
        "Niedźwiedzia",
        "Parafialna",
        "Przybyszewskiego",
    ]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    exe_start_time = time.time()
    tabu(graph, start, stops, "t", start_time)
    exe_end_time = time.time()
    print("5 stops: ", exe_end_time - exe_start_time, "\n")

    start = "KROMERA"
    stops = ["GALERIA DOMINIKAŃSKA"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    exe_start_time = time.time()
    tabu(graph, start, stops, "p", start_time)
    exe_end_time = time.time()
    print("1 stop: ", exe_end_time - exe_start_time, "\n")

    start = "KROMERA"
    stops = ["PL. GRUNWALDZKI", "Rynek"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    exe_start_time = time.time()
    tabu(graph, start, stops, "p", start_time)
    exe_end_time = time.time()
    print("2 stops: ", exe_end_time - exe_start_time, "\n")

    start = "KROMERA"
    stops = ["Katedra", "GALERIA DOMINIKAŃSKA", "Niedźwiedzia"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    tabu(graph, start, stops, "p", start_time)
    exe_end_time = time.time()
    print("3 stops: ", exe_end_time - exe_start_time, "\n")


def tabu_time_comparison(graph, opt, tabu_function):

    start = "KROMERA"
    stops = ["GALERIA DOMINIKAŃSKA"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    run_tabu(graph, start, stops, opt, start_time, tabu_function)

    start = "KROMERA"
    stops = ["PL. GRUNWALDZKI", "Rynek"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    run_tabu(graph, start, stops, opt, start_time, tabu_function)

    start = "KROMERA"
    stops = ["Katedra", "GALERIA DOMINIKAŃSKA", "Niedźwiedzia"]
    start_time = datetime.timedelta(hours=10, minutes=00, seconds=00)
    run_tabu(graph, start, stops, opt, start_time, tabu_function)


def run_all_tabu(graph):
    tabu_time_comparison(graph, "all", tabu)
    tabu_time_comparison(graph, "all", tabu_b)
    tabu_time_comparison(graph, "all", tabu_c)
    tabu_time_comparison(graph, "all", tabu_d)


if __name__ == "__main__":
    gg = get_graph_dict()
    run_all_tabu(gg)


