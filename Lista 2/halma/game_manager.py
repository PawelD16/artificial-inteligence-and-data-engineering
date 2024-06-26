from halma.base_game_engine import BaseGameEngine, make_move
from outputs.base_interface import BaseInterface


class GameManager:
    def __init__(
        self, game_engine: BaseGameEngine, output_interface: BaseInterface
    ) -> None:
        self.__game_engine: BaseGameEngine = game_engine
        self.__output_interface: BaseInterface = output_interface

    def start_game(self) -> None:
        no_moves_counter_in_row = 0
        turn = 1

        while (
            not (has_current_player_won := self.__game_engine.check_if_current_player_won())
            # and no_moves_counter_in_row < self.__game_engine.get_player_count()
        ):
            current_player = self.__game_engine.get_current_player()
            current_enemy = self.__game_engine.get_enemy_of_player(current_player)

            self.__output_interface.show_turn(turn)
            self.__output_interface.show_current_player(current_player)
            self.__output_interface.show_current_enemy(current_enemy)

            move_to_make = current_player.make_move(current_enemy, self.__game_engine)

            # no moves made
            if (
                move_to_make is None
                or move_to_make.get_starting_field() is None
                or move_to_make.get_finishing_field() is None
            ):
                no_moves_counter_in_row += 1
            # illegal move
            elif not make_move(move_to_make):
                raise Exception(
                    f"Illegal move made by {current_player}."
                )
            # move made
            else:
                no_moves_counter_in_row = 0

            self.__output_interface.display()
            self.__game_engine.change_player_turn()
            turn += 1

        # if nobody won, then it's a draw
        if not has_current_player_won:
            self.__output_interface.on_draw()
            return

        self.__output_interface.on_player_won(self.__game_engine.get_current_player())

    def __str__(self) -> str:
        return str(self.__game_engine)
