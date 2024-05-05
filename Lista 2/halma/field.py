from halma.enums import FieldState, PlayerType


class Field:
    def __init__(
        self,
        x: int,
        y: int,
        field_state: FieldState = FieldState.EMPTY,
        base_of: PlayerType = None,
        occupied_by: PlayerType = None,
    ) -> None:
        self.__x: int = x
        self.__y: int = y
        self.__base_of: PlayerType = base_of
        self.__field_state: FieldState = field_state
        self.__occupied_by: PlayerType = occupied_by

    def occupy_if_possible(self, player_type: PlayerType) -> bool:
        if not self.can_be_occupied():
            return False

        self.__field_state = FieldState.OCCUPIED
        self.__occupied_by = player_type

        return True

    def free_if_possible(self) -> bool:
        if self.can_be_occupied():
            return False

        self.__field_state = FieldState.EMPTY
        self.__occupied_by = None

        return True

    def get_field_state(self) -> FieldState:
        return self.__field_state

    def can_be_occupied(self) -> bool:
        return self.__field_state == FieldState.EMPTY and self.__occupied_by is None

    def base_of(self) -> PlayerType:
        return self.__base_of

    def occupied_by(self) -> PlayerType | None:
        return self.__occupied_by

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def set_x(self, x: int) -> None:
        self.__x = x

    def set_y(self, y: int) -> None:
        self.__y = y

    def set_base_of(self, player_type: PlayerType) -> bool:
        if self.occupy_if_possible(player_type):
            self.__base_of = player_type
            return True

        return False

    def __str__(self) -> str:
        if self.__field_state == FieldState.EMPTY:
            return "0"

        return str(int(self.__occupied_by))
