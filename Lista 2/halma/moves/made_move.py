from halma.enums import PlayerType
from halma.field import Field


class MadeMove:
    def __init__(
        self,
        starting_field: Field,
        finishing_field: Field,
        player_type: PlayerType,
        move_quality: float,
    ) -> None:
        if player_type is None or finishing_field is None or starting_field is None:
            raise ValueError(
                f"Player type, starting field and finishing field for made move cannot be None. "
                f"Starting field: {starting_field}, finishing field: {finishing_field}, player type: {player_type}"
            )

        if not (
            starting_field.occupied_by() == player_type
            and finishing_field.can_be_occupied()
        ):
            raise ValueError(
                "Invalid move."
                f"Starting fild: {starting_field}, finishing field: {finishing_field}, player type: {player_type}"
            )

        self.__starting_field: Field = starting_field
        self.__finishing_field: Field = finishing_field
        self.__player_type: PlayerType = player_type
        self.__move_quality: float = move_quality

    def get_finishing_field(self) -> Field:
        return self.__finishing_field

    def get_starting_field(self) -> Field:
        return self.__starting_field

    def get_move_value(self) -> float:
        return self.__move_quality

    def get_player_type(self) -> PlayerType:
        return self.__player_type


def build_made_move(
    starting_field: Field,
    finishing_field: Field,
    player_type: PlayerType,
    move_quality: float,
) -> MadeMove | None:
    try:
        return MadeMove(starting_field, finishing_field, player_type, move_quality)
    except ValueError:
        return None
