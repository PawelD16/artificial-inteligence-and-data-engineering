from abc import ABC
from typing import Callable

from halma.enums import PlayerType
from halma.field import Field
from players.base_player import BasePlayer


class HeuristicPlayer(BasePlayer, ABC):
    def __init__(
        self, player_type: PlayerType, heuristic_fn: Callable[[Field, Field], float]
    ) -> None:
        super().__init__(player_type)
        self.__heuristic_fn: Callable[[Field, Field], float] = heuristic_fn

    def get_heuristic_fn(self) -> Callable[[Field, Field], float]:
        return self.__heuristic_fn

    def __str__(self) -> str:
        return (
            f"Player type: {self._player_type}, "
            f"heuristic: {self.__heuristic_fn}, "
            f"base root: x:{self._base_root.get_x()}; y:{self._base_root.get_y()}"
        )
