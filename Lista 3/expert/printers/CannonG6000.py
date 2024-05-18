from __future__ import annotations

from typing import List

from experta import KnowledgeEngine

from facts.components import ComponentTypeG6000, get_all_component_types_g6000
from knowledge.G6000 import CannonG6000ProblemKnowledgeBase
from printers.Printer import Printer


class CannonG6000(Printer):

    def __init__(self) -> None:
        super().__init__(get_all_component_types_g6000())

    # only one with children currently
    def get_child_components(
        self, component: ComponentTypeG6000
    ) -> List[ComponentTypeG6000]:
        if component == ComponentTypeG6000.AnyPaperTray:
            return [
                ComponentTypeG6000.BacksidePaperTray,
                ComponentTypeG6000.FrontCassette,
            ]

        return []

    def get_knowledge_engine(self) -> KnowledgeEngine:
        return CannonG6000ProblemKnowledgeBase()
