from datetime import timedelta
from typing import Dict, List

from connection_node import Edge
from utils import generic_optimisation_function, calculate_cost_simple


def dijkstra_t(
        graph: Dict[str, List[Edge]],
        start: str,
        goal: str,
        start_time: timedelta
):
    def dijkstra_inner(edge, new_cost):
        return new_cost

    return generic_optimisation_function(graph, start, goal, start_time, dijkstra_inner, calculate_cost_simple)

