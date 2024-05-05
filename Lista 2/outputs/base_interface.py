from abc import ABC, abstractmethod

from halma.game_board import GameBoard
from players.base_player import BasePlayer


class BaseInterface(ABC):

    def __init__(self, game_board: GameBoard) -> None:
        self._game_board = game_board

    @abstractmethod
    def display(self) -> None:
        pass

    @abstractmethod
    def on_player_won(self, player: BasePlayer) -> None:
        pass

    @abstractmethod
    def on_draw(self) -> None:
        pass

    @abstractmethod
    def show_current_player(self, player: BasePlayer) -> None:
        pass

    @abstractmethod
    def show_current_enemy(self, player: BasePlayer) -> None:
        pass

    @abstractmethod
    def show_turn(self, turn: int) -> None:
        pass
