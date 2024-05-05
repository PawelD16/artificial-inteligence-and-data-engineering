from typing import List

from halma.enums import PlayerType
from halma.field import Field


class PossibleMove:
    def __init__(
        self, starting_field: Field, moves: List[Field], player_type: PlayerType
    ) -> None:
        if player_type is None:
            raise ValueError(
                f"Player type for starting field of possible move cannot be None. "
                f"Starting field: {starting_field}, moves: {moves}, player_type: {player_type}"
            )

        self.__starting_field = starting_field
        self.__moves: List[Field] = moves
        self.__player_type: PlayerType = player_type

    def get_singular_moves(self) -> List[Field]:
        return self.__moves

    def get_player_type(self) -> PlayerType:
        return self.__player_type

    def get_starting_field(self) -> Field:
        return self.__starting_field

    def get_last_field_of_moves(self) -> Field | None:
        return self.__moves[-1]

    def __str__(self) -> str:
        to_return = f"Starting: (x: {self.__starting_field.get_x()}, y: {self.__starting_field.get_y()}). Singular: "
        for singular in self.__moves:
            to_return += f"(x: {singular.get_x()}, y: {singular.get_y()})"

        return to_return
