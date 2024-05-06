import copy
from collections import deque
from typing import List, Self

from halma.base_game_engine import BaseGameEngine
from halma.enums import PlayerType, PlayerCount
from halma.game_board import GameBoard
from players.base_player import BasePlayer


class GameEngine(BaseGameEngine):
    def __init__(
        self,
        player_count: PlayerCount,
        players: List[BasePlayer],
        game_board: GameBoard,
    ) -> None:
        if len(players) != len(player_count.player_types):
            raise ValueError(
                f"""Incorrect number of players. 
                Game engine was set to  {len(player_count.player_types)}, but received {len(players)} players."""
            )

        self.__player_count: PlayerCount = player_count
        self.__game_board: GameBoard = game_board
        self.__set_all_starting_pieces(players, player_count)
        self.__players_queue: deque[BasePlayer] = deque(players)
        self.__is_game_over: bool = False

    def get_player_count(self) -> int:
        return len(self.__players_queue)

    def get_enemy_of_player(self, player: BasePlayer) -> BasePlayer:
        index = self.__players_queue.index(player)
        length = len(self.__players_queue)

        return self.__players_queue[(length // 2 + index) % length]

    def get_board(self) -> GameBoard:
        return self.__game_board

    def is_game_over(self) -> bool:
        return self.check_if_current_player_won()

    def change_player_turn(self) -> None:
        first_element = self.__players_queue.popleft()
        self.__players_queue.append(first_element)

    def get_current_player(self) -> BasePlayer:
        return self.__players_queue[0]

    def check_if_current_player_won(self) -> bool:
        return self.get_board().check_if_enemy_base_taken_over(
            self.__players_queue[0].get_type(),
            self.__players_queue[len(self.__players_queue) // 2].get_type(),
        )

    def __set_all_starting_pieces(
        self, players: List[BasePlayer], player_count: PlayerCount
    ) -> None:
        for player in players:
            self.__set_starting_pieces(player_count.piece_count, player.get_type())
            player.set_base_root(self.__game_board.get_field(0, 0))

            for _ in range(player_count.board_rotations):
                self.__game_board.rotate_90_degrees()

    def __find_player_by_player_type(self, player_type: PlayerType) -> BasePlayer:
        for player in self.__players_queue:
            if player.get_type == player_type:
                return player

        raise Exception(
            f"Player with type {player_type} doesn't exist in player_queue: {self.__players_queue}."
        )

    def __set_starting_pieces(
        self, max_piece_count: int, player_type: PlayerType
    ) -> None:
        pieces_placed = 0
        row_num = 0

        def try_setting_board_field(pieces_placed_inner: int, x: int, y: int) -> bool:
            if self.__game_board.is_within_bounds(x, y):
                return (
                    pieces_placed_inner < max_piece_count
                    and self.__game_board.get_field(x, y).set_base_of(player_type)
                )

            return False

        while pieces_placed < max_piece_count:
            for i in range(row_num // 2 + 1, 0, -1):
                if try_setting_board_field(pieces_placed, i - 1, row_num - i):
                    pieces_placed += 1

                if try_setting_board_field(pieces_placed, row_num - i, i - 1):
                    pieces_placed += 1

            row_num += 1

    def __str_all_players(self) -> str:
        return "\n\t".join(map(str, list(self.__players_queue)))

    def __str__(self) -> str:
        return (
            f"Players: \n[\n\t{self.__str_all_players()}\n], \n"
            f"Player count: {self.__player_count}, \n"
            f"Board: \n {self.__game_board} \n"
        )
