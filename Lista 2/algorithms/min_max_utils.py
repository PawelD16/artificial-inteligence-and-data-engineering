from halma.game_board import GameBoard
from players.base_player import BasePlayer

IN_ENEMY_BASE_MULTIPLIER = 20


# simplification that the goal is for example the root of the base
def score_for_game_state(
    game_board: GameBoard, player: BasePlayer, enemy: BasePlayer
) -> float:
    quality = 0

    for x in range(game_board.get_size()):
        for y in range(game_board.get_size()):
            calculated_quality = 0

            if game_board.get_field(x, y).occupied_by() == player.get_type():
                calculated_quality = - player.get_heuristic_fn()(game_board.get_field(x, y), enemy.get_base_root())

                # if the piece is already in enemy base try focusing on other pieces to get there!
                if game_board.get_field(x, y).base_of() == enemy.get_type():
                    calculated_quality /= IN_ENEMY_BASE_MULTIPLIER

            elif game_board.get_field(x, y).occupied_by() == enemy.get_type():
                calculated_quality = player.get_heuristic_fn()(game_board.get_field(x, y), player.get_base_root())

            quality += calculated_quality
    return quality
