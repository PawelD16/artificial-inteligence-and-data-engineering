from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict

from experta import KnowledgeEngine

from facts.components import ComponentState, ComponentType
from facts.error_code import ErrorCode


class Printer(ABC):
    def __init__(self, components: List[ComponentType]) -> None:
        self.__components: Dict[ComponentType, ComponentState] = {
            key: ComponentState.OK for key in components
        }
        self.__error_code: ErrorCode | None = None

    @abstractmethod
    def get_child_components(self, component: ComponentType) -> List[ComponentType]:
        pass

    @abstractmethod
    def get_knowledge_engine(self) -> KnowledgeEngine:
        pass

    def break_component(self, component_to_break: ComponentType) -> bool:
        found = False

        # Iterating over the entire dictionary because many flags may work!
        for comp in self.__components.keys():
            if (
                component_to_break == comp
                or component_to_break in self.get_child_components(comp)
            ):
                self.__components[comp] = ComponentState.ERROR
                found = True

        return found

    def get_broken_components(self) -> List[ComponentType]:
        return [
            component
            for component, state in self.__components.items()
            if state == ComponentState.ERROR
        ]

    def remove_error(self) -> None:
        self.__error_code = None

    def set_error_code(self, error_code: ErrorCode) -> None:
        self.__error_code = error_code

    def get_error_code(self) -> ErrorCode | None:
        return self.__error_code

    def __str__(self) -> str:
        components_str = []
        for key, value in self.__components.items():
            components_str.append(f"{key}: {value}")

        dict_str = "{\n  " + ",\n  ".join(components_str) + "\n}"
        return f"Components: {dict_str}, ErrorCode: {self.__error_code}"
