from enum import Enum
from typing import List

from experta import Fact


class ComponentType(Enum):
    pass


class ComponentTypeG6000(ComponentType):
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


class ComponentTypeDcp770CW(ComponentType):
    PaperTray = 1
    TemperatureSensor = 2
    WasteInkCartridge = 3
    PrintHead = 4
    PaperTransportModule = 5
    Scanner = 6
    PCB = 7
    PaperPositionSensor = 8


def get_all_component_types_g6000() -> List[ComponentTypeG6000]:
    return list(ComponentTypeG6000.__members__.values())


def get_all_component_types_dcp_770_cw() -> List[ComponentTypeDcp770CW]:
    return list(ComponentTypeDcp770CW.__members__.values())


class ComponentState(Enum):
    OK = 1
    ERROR = 2


class BrokenComponent(Fact):
    """Information about the printer component"""
    pass
