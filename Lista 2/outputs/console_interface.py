from typing import Callable

from halma.game_board import GameBoard
from outputs.base_interface import BaseInterface
from players.base_player import BasePlayer


class ConsoleInterface(BaseInterface):

    def __init__(self, game_board: GameBoard) -> None:
        super().__init__(game_board)

    def display(self) -> None:
        print(self._game_board)

    def on_player_won(self, player: BasePlayer) -> None:
        print(f"{player} won!")

    def on_draw(self) -> None:
        print("DRAW!")

    def show_current_player(self, player: BasePlayer) -> None:
        print(f"Current player: {player.get_type().color_fn(str(player))}")

    def show_current_enemy(self, player: BasePlayer) -> None:
        print(f"Current enemy: {player.get_type().color_fn(str(player))}")

    def show_turn(self, turn: int) -> None:
        print(f"Turn number: {turn}")
