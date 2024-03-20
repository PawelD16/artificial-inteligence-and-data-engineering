from datetime import timedelta


class Connection:
    def __init__(
            self,
            start: str,
            end: str,
            line: str,
            departure_time: timedelta,
            arrival_time: timedelta,
            start_lat: float,
            start_lon: float,
            end_lat: float,
            end_lon: float
    ):
        self.start = start
        self.end = end
        self.line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.end_lat = end_lat
        self.end_lon = end_lon

    def __repr__(self):
        return f"Connection({self.start} to {self.end}, line {self.line})"


class Edge:
    def __init__(
            self,
            neighbour: str,
            line: str,
            departure_time: timedelta,
            arrival_time: timedelta,
            start_lat: float,
            start_lon: float,
            end_lat: float,
            end_lon: float
    ):
        self.neighbour = neighbour
        self.line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.end_lat = end_lat
        self.end_lon = end_lon

    def __repr__(self):
        return f"Node(neighbour: {self.neighbour}, line: {self.line})"


def convert_from_connection_to_node(name: str, connection: Connection) -> Edge:
    return Edge(
        name,
        connection.line,
        connection.departure_time,
        connection.arrival_time,
        connection.start_lat,
        connection.start_lon,
        connection.end_lat,
        connection.end_lon
    )
