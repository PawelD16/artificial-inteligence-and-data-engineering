from halma.base_game_engine import BaseGameEngine, make_move
from outputs.base_interface import BaseInterface
from players.base_player import BasePlayer


class GameManager:
    def __init__(
        self, game_engine: BaseGameEngine, output_interface: BaseInterface
    ) -> None:
        self.__game_engine: BaseGameEngine = game_engine
        self.__output_interface: BaseInterface = output_interface

    def start_game(self) -> BasePlayer | None:
        no_moves_counter = 0

        while (
            not self.__game_engine.check_if_current_player_won()
            and no_moves_counter < self.__game_engine.get_player_count()
        ):

            current_player = self.__game_engine.get_current_player()
            current_enemy = self.__game_engine.get_enemy_of_player(current_player)

            self.__output_interface.show_current_player(current_player)
            self.__output_interface.show_current_enemy(current_enemy)

            move_to_make = self.__game_engine.get_current_player().make_move(
                current_enemy, self.__game_engine
            )

            if (
                move_to_make is None
                or move_to_make.get_starting_field() is None
                or move_to_make.get_finishing_field() is None
            ):
                no_moves_counter += 1
            elif not make_move(move_to_make):
                raise Exception(
                    f"Illegal move made by {self.__game_engine.get_current_player()}."
                )

            self.__output_interface.display()
            self.__game_engine.change_player_turn()

        if self.__game_engine.check_if_current_player_won():
            self.__output_interface.on_player_won(
                self.__game_engine.get_current_player()
            )
            return self.__game_engine.get_current_player()

        self.__output_interface.on_draw()
        return None

    def __str__(self) -> str:
        return str(self.__game_engine)
