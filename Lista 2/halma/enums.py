from enum import Enum
from typing import List


class PlayerType(Enum):
    PLAYER1 = 1
    PLAYER2 = 2
    PLAYER3 = 3
    PLAYER4 = 4

    def __int__(self):
        return self.value


class PlayerCount(Enum):
    TWO_PLAYERS = 0, [PlayerType.PLAYER1, PlayerType.PLAYER2], 19, 2
    FOUR_PLAYERS = (
        1,
        [
            PlayerType.PLAYER1,
            PlayerType.PLAYER2,
            PlayerType.PLAYER3,
            PlayerType.PLAYER4,
        ],
        13,
        1,
    )

    def __new__(
        cls,
        value: int,
        player_types: List[PlayerType],
        piece_count: int,
        board_rotations: int,
    ):
        member = object.__new__(cls)
        member._value_ = value
        member.player_types = player_types
        member.piece_count = piece_count
        member.board_rotations = board_rotations

        return member

    def __int__(self):
        return self.value


class FieldState(Enum):
    EMPTY = 1
    OCCUPIED = 2

    def __int__(self):
        return self.value


def find_player_count_enum_by_player_count(player_count_int: int) -> PlayerCount | None:
    for player_count_enum in PlayerCount:
        if len(player_count_enum.player_types) == player_count_int:
            return player_count_enum

    return None
