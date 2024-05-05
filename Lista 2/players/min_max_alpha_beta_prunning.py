import math
from typing import Callable

from algorithms.min_max_utils import score_for_game_state
from halma.base_game_engine import (
    BaseGameEngine,
    make_possible_move,
    undo_possible_move,
)
from halma.enums import PlayerType
from halma.field import Field
from halma.moves.made_move import MadeMove, build_made_move
from players.base_player import BasePlayer
from players.heuristic_player import HeuristicPlayer


class MinMaxAlphaBetaPrunedPlayer(HeuristicPlayer):
    def __init__(
        self,
        player_type: PlayerType,
        heuristic_fn: Callable[[Field, Field], float],
        min_max_depth: int,
        is_maximizing: bool,
    ) -> None:
        super().__init__(player_type, heuristic_fn)

        self.__min_max_depth = min_max_depth
        self.__is_maximizing = is_maximizing

    def make_move(
        self, enemy_player: BasePlayer, game_engine: BaseGameEngine
    ) -> MadeMove:
        (finish, quality, start) = self.__minmax_α_β_pruning(
            self.__min_max_depth,
            self.__is_maximizing,
            game_engine,
            self,
            enemy_player,
            -math.inf,
            math.inf,
        )
        return build_made_move(start, finish, self._player_type, quality)

    def __minmax_α_β_pruning(
        self,
        depth: int,
        is_maximizing_player: bool,
        game_engine: BaseGameEngine,
        player: BasePlayer,
        enemy: BasePlayer,
        alpha: float,
        beta: float,
    ) -> (Field | None, float, Field | None):

        if depth == 0 or game_engine.is_game_over():
            return (
                None,
                score_for_game_state(game_engine.get_board(), player, enemy),
                None,
            )

        if is_maximizing_player:
            best_quality = -math.inf
            best_finish_field = None
            best_start_field = None

            for move in game_engine.get_board().get_all_allowed_moves(
                player.get_type()
            ):
                if not make_possible_move(move):
                    raise Exception(f"Can't make move {move}")

                (_, quality, _) = self.__minmax_α_β_pruning(
                    depth - 1, False, game_engine, player, enemy, alpha, beta
                )

                if quality > best_quality:
                    best_quality = quality
                    best_finish_field = move.get_last_field_of_moves()
                    best_start_field = move.get_starting_field()

                if not undo_possible_move(move):
                    raise Exception(f"Can't undo move {move}")

                alpha = max(best_quality, alpha)
                if beta <= alpha:
                    break

            return best_finish_field, best_quality, best_start_field
        else:
            best_quality = math.inf
            best_finish_field = None
            best_start_field = None

            for move in game_engine.get_board().get_all_allowed_moves(
                enemy.get_type()
            ):
                if not make_possible_move(move):
                    raise Exception(f"Can't make move {move}")

                (_, quality, _) = self.__minmax_α_β_pruning(
                    depth - 1, True, game_engine, player, enemy, alpha, beta
                )

                if quality < best_quality:
                    best_quality = quality
                    best_finish_field = move.get_last_field_of_moves()
                    best_start_field = move.get_starting_field()

                if not undo_possible_move(move):
                    raise Exception(f"Can't undo move {move}")

                beta = min(best_quality, beta)
                if beta <= alpha:
                    break

            return best_finish_field, best_quality, best_start_field
