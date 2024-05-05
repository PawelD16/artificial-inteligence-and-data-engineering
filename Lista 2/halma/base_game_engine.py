from abc import ABC, abstractmethod

from halma.game_board import GameBoard
from halma.moves.made_move import MadeMove
from halma.moves.possible_move import PossibleMove
from players.base_player import BasePlayer


def undo_possible_move(move: PossibleMove) -> bool:
    return (
        move.get_starting_field().occupy_if_possible(move.get_player_type())
        and move.get_last_field_of_moves().free_if_possible()
    )


def make_possible_move(move: PossibleMove) -> bool:
    return (
        move.get_starting_field().free_if_possible()
        and move.get_last_field_of_moves().occupy_if_possible(move.get_player_type())
    )


def make_move(move: MadeMove) -> bool:
    return (
        move.get_starting_field().free_if_possible()
        and move.get_finishing_field().occupy_if_possible(move.get_player_type())
    )


class BaseGameEngine(ABC):

    @abstractmethod
    def get_board(self) -> GameBoard:
        pass

    @abstractmethod
    def get_player_count(self) -> int:
        pass

    # @abstractmethod
    # def copy_with_new_board(self, game_board: GameBoard) -> Self:
    #     pass

    @abstractmethod
    def is_game_over(self) -> bool:
        pass

    @abstractmethod
    def check_if_current_player_won(self) -> bool:
        pass

    @abstractmethod
    def get_current_player(self) -> BasePlayer:
        pass

    @abstractmethod
    def change_player_turn(self) -> bool:
        pass

    @abstractmethod
    def get_enemy_of_player(self, player: BasePlayer) -> BasePlayer:
        pass
