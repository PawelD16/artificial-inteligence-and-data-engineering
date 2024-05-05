import math

from halma.field import Field


def manhattan_distance(current: Field, goal: Field) -> float:
    return abs(current.get_x() - goal.get_x()) + abs(current.get_y() - goal.get_y())


def euclidean_distance(current: Field, goal: Field) -> float:
    return math.sqrt((current.get_x() - goal.get_x()) ** 2 + (current.get_y() - goal.get_y()) ** 2)


def chebyshev_distance(current: Field, goal: Field) -> float:
    return max(abs(current.get_x() - goal.get_x()), abs(current.get_y() - goal.get_y()))
