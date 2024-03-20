# to trzeba przeformatowac, pewnie najlepiej z chata
def print_path(cost, path, arrival_times, departure_times, lines):
    if len(path) > 1:
        print(path[0])
        print(lines[1], ": ", departure_times[1], " - ", end="")

        prev_line = lines[1]
        prev_arrival_time = arrival_times[1]
        prev_stop = path[1]

        for i in range(len(path)):
            if i > 0:
                if prev_line != lines[i]:
                    if i > 1:
                        print(prev_arrival_time)
                        print(prev_stop)
                    print(lines[i], ": ", departure_times[i], " - ", end="")
                prev_line = lines[i]
                prev_arrival_time = arrival_times[i]
                prev_stop = path[i]
        print(arrival_times[len(path) - 1])
        print(prev_stop)


def print_path_all(cost, path, arrival_times, departure_times, lines):
    if len(path) > 1:
        print(path[0])
        for i in range(len(path)):
            if i > 0:
                print(lines[i], ": ", departure_times[i], " - ", arrival_times[i])
                print(path[i])
