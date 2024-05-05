import copy

from halma.game_board import GameBoard
from players.base_player import BasePlayer


# simplification that the goal is for example the root of the base
def score_for_game_state(
    game_board: GameBoard, player: BasePlayer, enemy: BasePlayer
) -> float:
    quality = 0

    for x in range(game_board.get_size()):
        for y in range(game_board.get_size()):
            if game_board.get_field(x, y).occupied_by() == player.get_type():
                quality -= player.get_heuristic_fn()(
                    game_board.get_field(x, y), enemy.get_base_root()
                )

            elif game_board.get_field(x, y).occupied_by() == enemy.get_type():
                quality += player.get_heuristic_fn()(
                    game_board.get_field(x, y), player.get_base_root()
                )

    return quality


def minimax_with_alpha_beta_prunning(
    depth,
    isMaximizinPlayer,
    game,
    player,
    hueristic_player_1,
    alpha,
    heuristic_player_2,
    beta,
):
    if depth == 0 or game.is_over():
        return score_for_game_state()

    if isMaximizinPlayer:
        bestValue = float("inf")
        bestMove = None
        board_before_move = copy.deepcopy(game.board)
        for move in game.all_possible_moves:
            game.make_move
            (move, quality) = minimax_with_alpha_beta_prunning(
                depth - 1,
                False,
                game,
                hueristic_player_1,
                alpha,
                heuristic_player_2,
                beta,
            )
            if quality < bestValue:
                bestValue = quality
                bestMove = move
            game.undo_move()
            alpha = max(alpha, bestValue)
            if beta <= alpha:
                break
        return bestMove, bestValue
    else:
        bestValue = float("-inf")
        bestMove = None
        board_before_move = copy.deepcopy(game.board)
        for move in game.all_possible_moves:
            game.make_move
            (move, quality) = minmax(
                depth - 1,
                True,
                game,
                hueristic_player_1,
                alpha,
                heuristic_player_2,
                beta,
            )
            if quality < bestValue:
                bestValue = quality
                bestMove = move
            game.undo_move()
            beta = min(beta, bestValue)
            if beta <= alpha:
                break
        return bestMove, bestValue
