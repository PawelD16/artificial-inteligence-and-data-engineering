from abc import ABC, abstractmethod
from typing import Self, Callable

from halma.enums import PlayerType
from halma.field import Field
from halma.moves.made_move import MadeMove


class BasePlayer(ABC):
    def __init__(self, player_type: PlayerType, heuristic_fn: Callable[[Field, Field], float]) -> None:
        self._player_type: PlayerType = player_type
        self._base_root: Field | None = None
        self.__heuristic_fn: Callable[[Field, Field], float] = heuristic_fn

    def get_type(self) -> PlayerType:
        return self._player_type

    def set_base_root(self, base_root: Field) -> None:
        self._base_root = base_root

    def get_base_root(self) -> Field | None:
        return self._base_root

    def get_heuristic_fn(self) -> Callable[[Field, Field], float]:
        return self.__heuristic_fn

    @abstractmethod
    def make_move(self, enemy_player: Self, game_engine: "BaseGameEngine") -> MadeMove:
        pass

    def __str__(self) -> str:
        return (
            f"Player type: {self._player_type}, "
            f"heuristic: {self.__heuristic_fn}, "
            f"base root: x:{self._base_root.get_x()}; y:{self._base_root.get_y()}"
        )
