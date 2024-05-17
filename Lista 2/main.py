from algorithms.heuristics import manhattan_distance, euclidean_distance, chebyshev_distance
from halma.enums import PlayerCount
from halma.game_board import GameBoard
from halma.game_engine import GameEngine
from halma.game_manager import GameManager
from outputs.console_interface import ConsoleInterface
from players.min_max_alpha_beta_prunning import MinMaxAlphaBetaPrunedPlayer
from players.random_player import RandomPlayer


def main() -> None:
    board_size = 16
    player_count = PlayerCount.FOUR_PLAYERS

    game_board = GameBoard(board_size)

    players = [
        MinMaxAlphaBetaPrunedPlayer(player_count.player_types[0], euclidean_distance, 2, True),
        MinMaxAlphaBetaPrunedPlayer(player_count.player_types[1], manhattan_distance, 2, True),
        MinMaxAlphaBetaPrunedPlayer(player_count.player_types[2], chebyshev_distance, 2, True),
        RandomPlayer(player_count.player_types[3], euclidean_distance)
    ]

    game_engine = GameEngine(player_count, players, game_board)
    output = ConsoleInterface(game_engine.get_board())

    game_manager = GameManager(game_engine, output)
    game_manager.start_game()


if __name__ == "__main__":
    main()
