from random import choice
from typing import Self

from halma.base_game_engine import BaseGameEngine
from halma.enums import PlayerType
from halma.field import Field
from halma.moves.made_move import MadeMove, build_made_move
from players.base_player import BasePlayer


class RandomPlayer(BasePlayer):
    def __init__(self, player_type: PlayerType) -> None:
        super().__init__(player_type)

    def make_move(self, enemy_player: Self, game_engine: BaseGameEngine) -> MadeMove:
        (starting_field, finishing_field) = self.__choose_random_move(game_engine)

        return build_made_move(starting_field, finishing_field, self.get_type(), 0)

    def __choose_random_move(
        self, game_engine: BaseGameEngine
    ) -> (Field | None, Field | None):
        all_moves = game_engine.get_board().get_all_allowed_moves(self.get_type())
        chosen = choice(choice(all_moves))

        return chosen.get_starting_field(), chosen.get_last_field_of_moves()
