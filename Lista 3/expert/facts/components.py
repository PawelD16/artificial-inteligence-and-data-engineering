from enum import IntFlag, Enum
from typing import List

from experta import Fact, Field


class ComponentType(IntFlag):
    InkCartridge = 1
    PrintHead = 2
    PrintHeadHolder = 3
    PaperTransportModule = 4
    Connectivity = 5
    PrintingMechanism = 6,
    FrontCassette = 7
    BacksidePaperTray = 8
    AnyPaperTray = FrontCassette | BacksidePaperTray
    WasteInkContainer = 9


def get_all_component_types() -> List[ComponentType]:
    return list(ComponentType.__members__.values())


class ComponentState(Enum):
    OK = 1
    ERROR = 2


class BrokenComponent(Fact):
    """Information about the printer component"""
    component_type = Field(ComponentType, default=lambda: None)
