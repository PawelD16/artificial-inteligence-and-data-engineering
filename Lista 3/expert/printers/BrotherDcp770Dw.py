from typing import List

from experta import KnowledgeEngine

from facts.components import ComponentTypeDcp770CW, get_all_component_types_dcp_770_cw
from facts.error_code import ErrorCodeDcp770cw
from knowledge.Dcp770Dw import BrotherDcp770DwProblemKnowledgeBase
from printers.Printer import Printer


class BrotherDcp770Dw(Printer):

    def __init__(self, error_code: ErrorCodeDcp770cw = None) -> None:
        super().__init__(get_all_component_types_dcp_770_cw(), error_code)

    # no nested components
    def get_child_components(self, component: ComponentTypeDcp770CW) -> List[ComponentTypeDcp770CW]:
        return []

    def get_knowledge_engine(self) -> KnowledgeEngine:
        return BrotherDcp770DwProblemKnowledgeBase()
