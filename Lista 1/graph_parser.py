from typing import Dict, List

import pandas as pd
import datetime

from connection_node import Connection, convert_from_connection_to_node, Edge

columns = [
    "company",
    "line",
    "departure_time",
    "arrival_time",
    "start_stop",
    "end_stop",
    "start_stop_lat",
    "start_stop_lon",
    "end_stop_lat",
    "end_stop_lon"
]


def parse_time(time_str: str) -> datetime:
    day = 1
    hour, minute, second = map(int, time_str.split(":"))
    if hour >= 24:
        hour = hour % 24
        day += 1
    dt = datetime.datetime(2000, 1, day, hour, minute, second)
    return dt


def get_graph_dict() -> Dict[str, List[Edge]]:
    # reading a file
    file = "./connection_graph.csv"
    data = pd.read_csv(file, delimiter=",", dtype="unicode")
    # select columns
    data = data[columns]
    # parse time
    data["departure_time"] = data["departure_time"].apply(parse_time)
    data["arrival_time"] = data["arrival_time"].apply(parse_time)
    # create a dataframe
    dataframe = pd.DataFrame(data, columns=columns)

    edges = []
    for index, row in dataframe.iterrows():
        arrival_time = row["arrival_time"]
        departure_time = row["departure_time"]

        arrival_time_delta = datetime.timedelta(
            days=arrival_time.day,
            hours=arrival_time.hour,
            minutes=arrival_time.minute,
            seconds=arrival_time.second,
        )
        departure_time_delta = datetime.timedelta(
            days=departure_time.day,
            hours=departure_time.hour,
            minutes=departure_time.minute,
            seconds=departure_time.second,
        )
        # add edges to a list
        edges.append(
            Connection(
                row["start_stop"],
                row["end_stop"],
                row["line"],
                departure_time_delta,
                arrival_time_delta,
                row["start_stop_lat"],
                row["start_stop_lon"],
                row["end_stop_lat"],
                row["end_stop_lon"],
            )
        )

    graph_dict = {}
    for connection in edges:
        end_node = convert_from_connection_to_node(connection.end, connection)
        if connection.start in graph_dict:
            graph_dict[connection.start].append(end_node)
        else:
            graph_dict[connection.start] = [end_node]

        start_node = convert_from_connection_to_node(connection.start, connection)
        if connection.end in graph_dict:
            graph_dict[connection.end].append(start_node)
        else:
            graph_dict[connection.end] = [start_node]

    return graph_dict
