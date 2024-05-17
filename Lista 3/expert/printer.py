from __future__ import annotations

from typing import Dict, List

from facts.components import ComponentType, ComponentState
from facts.error_code import ErrorCode


class Printer:
    def __init__(self, components: List[ComponentType], error_code: ErrorCode = None) -> None:
        self.__components: Dict[ComponentType, ComponentState] = {key: ComponentState.OK for key in components}
        self.__error_code: ErrorCode | None = error_code

    def break_component(self, component: ComponentType) -> bool:
        if component not in self.__components:
            return False

        self.__components[component] = ComponentState.ERROR
        return True

    def get_broken_components(self) -> List[ComponentType]:
        return [component for component, state in self.__components.items() if state == ComponentState.ERROR]

    def remove_error(self) -> None:
        self.__error_code = None

    def set_error_code(self, error_code: ErrorCode) -> None:
        self.__error_code = error_code

    def get_error_code(self) -> ErrorCode | None:
        return self.__error_code
