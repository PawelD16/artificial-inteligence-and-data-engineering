from enum import Enum
from typing import List

from experta import Fact


class ComponentType(Enum):
    InkCartridge = 1,
    PrintHead = 2,
    PrintHeadHolder = 3,
    PaperTransportModule = 4,
    Connectivity = 5,
    PrintingMechanism = 6,
    WasteInkContainer = 7,
    FrontCassette = 8,
    BacksidePaperTray = 9,
    AnyPaperTray = 10,


# only one with children currently
def get_child_components(component: ComponentType) -> List[ComponentType]:
    if component == ComponentType.AnyPaperTray:
        return [ComponentType.BacksidePaperTray, ComponentType.FrontCassette]

    return []


def get_all_component_types() -> List[ComponentType]:
    return list(ComponentType.__members__.values())


class ComponentState(Enum):
    OK = 1
    ERROR = 2


class BrokenComponent(Fact):
    """Information about the printer component"""
    pass
