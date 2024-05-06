from typing import List, Tuple

from halma.enums import FieldState, PlayerType
from halma.field import Field
from halma.moves.possible_move import PossibleMove


class GameBoard:
    def __init__(self, size: int, initial_field_state: FieldState = FieldState.EMPTY):
        if size < 0:
            raise ValueError("x_size and y_size must be positive integers.")

        self.__size: int = size
        self.__game_board: List[List[Field]] = [
            [Field(x, y, initial_field_state) for x in range(size)] for y in range(size)
        ]
        self.__possible_move_directions: List[Tuple[int, int]] = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

    def check_if_enemy_base_taken_over(
        self, player: PlayerType, enemy_player: PlayerType
    ) -> bool:
        total_enemy_base_fields = 0
        total_player_pieces_in_enemy_base = 0
        total_enemy_pieces_in_enemy_base = 0

        for row in self.__game_board:
            for field in row:
                if field.base_of() == enemy_player:
                    total_enemy_base_fields += 1
                    
                    if field.occupied_by() == player:
                        total_player_pieces_in_enemy_base += 1
                    elif field.occupied_by() == enemy_player:
                        total_enemy_pieces_in_enemy_base += 1

        return (total_player_pieces_in_enemy_base > 0
                and total_enemy_base_fields == total_enemy_pieces_in_enemy_base + total_player_pieces_in_enemy_base)

    def get_field(self, x: int, y: int) -> Field:
        if not self.is_within_bounds(x, y):
            raise ValueError(f"x: {x} or y: {y} out of range.")

        return self.__game_board[x][y]

    def set_field(
        self,
        x: int,
        y: int,
        field_state: FieldState = FieldState.EMPTY,
        base_of: PlayerType = None,
        player_type: PlayerType = None,
    ) -> bool:
        if (
            not self.is_within_bounds(x, y)
            or not self.get_field(x, y).can_be_occupied()
        ):
            return False

        self.__game_board[x][y] = Field(x, y, field_state, base_of, player_type)
        return True

    # Jumping over your own pieces is allowed!
    def allowed_moves(self, x: int, y: int, enemy_player: PlayerType) -> List[PossibleMove]:
        if not self.is_within_bounds(x, y):
            raise ValueError(f"x: {x} or y: {y} out of range.")

        return self.__check_jumps(x, y, enemy_player) + self.__check_moves(x, y, enemy_player)

    def get_all_allowed_moves(
        self, player_type: PlayerType, enemy_player: PlayerType
    ) -> List[PossibleMove]:
        all_player_pieces: List[PossibleMove] = []

        for row in self.__game_board:
            for field in row:
                if field.occupied_by() == player_type:
                    allowed_moves = self.allowed_moves(field.get_x(), field.get_y(), enemy_player)
                    if len(allowed_moves) > 0:
                        all_player_pieces += allowed_moves

        return all_player_pieces

    def get_size(self) -> int:
        return self.__size

    def rotate_90_degrees(self) -> None:
        # rotating in place from
        # https://www.geeksforgeeks.org/rotate-a-matrix-by-90-degree-in-clockwise-direction-without-using-any-extra-space/
        s = self.__size

        for i in range(s // 2):
            for j in range(i, s - i - 1):
                temp = self.__game_board[i][j]
                self.__game_board[i][j] = self.__game_board[s - 1 - j][i]
                self.__game_board[s - 1 - j][i] = self.__game_board[s - 1 - i][s - 1 - j]
                self.__game_board[s - 1 - i][s - 1 - j] = self.__game_board[j][s - 1 - i]
                self.__game_board[j][s - 1 - i] = temp

        # update the x and y properties of each object to reflect new positions
        for x in range(s):
            for y in range(s):
                field = self.__game_board[x][y]
                field.set_x(x)
                field.set_y(y)

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.__size and 0 <= y < self.__size

    def __check_moves(self, x: int, y: int, enemy_player: PlayerType) -> List[PossibleMove]:
        possible_moves = []
        starting_field = self.get_field(x, y)

        for direction_x, direction_y in self.__possible_move_directions:
            checked_x, checked_y = x + direction_x, y + direction_y

            if (
                self.is_within_bounds(checked_x, checked_y)
                and (checked_field := self.get_field(checked_x, checked_y)).can_be_occupied()
            ):
                if not starting_field.base_of() == enemy_player or not checked_field.base_of() != enemy_player:
                    possible_moves.append(
                        PossibleMove(
                            starting_field,
                            [checked_field],
                            starting_field.occupied_by(),
                        )
                    )

        return possible_moves

    def __check_jumps(self, x: int, y: int, enemy_player: PlayerType) -> List[PossibleMove]:
        possible_jumps: List[PossibleMove] = []

        def __check_jumps_inner(
            inner_x: int,
            inner_y: int,
            current_moves: List[Field],
            current_already_checked: List[Tuple[Field, Field]],
            starting_field: Field,
        ) -> None:
            checked = current_already_checked

            for direction_x, direction_y in self.__possible_move_directions:
                jump_x, jump_y = inner_x + 2 * direction_x, inner_y + 2 * direction_y
                between_x, between_y = inner_x + direction_x, inner_y + direction_y

                if self.is_within_bounds(jump_x, jump_y):
                    current_move = (
                        checked_jump := self.get_field(inner_x, inner_y),
                        self.get_field(jump_x, jump_y),
                    )
                    checked = checked + [current_move]

                    if (
                        checked_jump.can_be_occupied()
                        and not (starting_field.base_of() == enemy_player and checked_jump.base_of() != enemy_player)
                        and not self.get_field(between_x, between_y).can_be_occupied()
                        and current_move not in current_already_checked
                    ):

                        new_current_moves = current_moves + [self.get_field(jump_x, jump_y)]
                        possible_jumps.append(
                            PossibleMove(
                                starting_field,
                                new_current_moves,
                                starting_field.occupied_by(),
                            )
                        )
                        __check_jumps_inner(
                            jump_x, jump_y, new_current_moves, checked, starting_field
                        )

        __check_jumps_inner(x, y, [], [], self.get_field(x, y))

        return possible_jumps

    def __str__(self):
        header = " ".join(f"{col:3}" for col in range(self.__size))
        separator = "  " + "---" * self.__size

        rows = []
        for x in range(self.__size):
            row = f"{x:2}|" + "".join(f"{str(self.get_field(x, y)):3}" for y in range(self.__size))
            rows.append(row)

        return f"   {header}\n{separator}\n" + "\n".join(rows) + f"\n{separator}\n"

