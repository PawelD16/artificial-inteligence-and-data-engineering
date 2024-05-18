from experta import KnowledgeEngine, Rule, OR

from facts.components import BrokenComponent, ComponentTypeDcp770CW
from facts.error_code import Error, ErrorCodeDcp770cw
from knowledge.utils import print_fault_and_solution


class BrotherDcp770DwProblemKnowledgeBase(KnowledgeEngine):

    @Rule(
        OR(
            OR(
                Error(code=ErrorCodeDcp770cw.E_30),
                Error(code=ErrorCodeDcp770cw.E_31),
                Error(code=ErrorCodeDcp770cw.E_32),
                Error(code=ErrorCodeDcp770cw.E_33),
                Error(code=ErrorCodeDcp770cw.E_34),
                Error(code=ErrorCodeDcp770cw.E_35),
                Error(code=ErrorCodeDcp770cw.E_36),
                Error(code=ErrorCodeDcp770cw.E_37),
                Error(code=ErrorCodeDcp770cw.E_38),
                Error(code=ErrorCodeDcp770cw.E_39),
                Error(code=ErrorCodeDcp770cw.E_3C),
                Error(code=ErrorCodeDcp770cw.E_3F),
            ),
            BrokenComponent(component_type=ComponentTypeDcp770CW.PaperTray),
        )
    )
    def paper_jammed(self) -> None:
        print_fault_and_solution(
            "The machine does not operate due to a paper jam.",
            "Remove jammed sheet from paper tray"
        )

    @Rule(
        OR(
            OR(
                Error(code=ErrorCodeDcp770cw.E_40),
                Error(code=ErrorCodeDcp770cw.E_42),
                Error(code=ErrorCodeDcp770cw.E_43),
                Error(code=ErrorCodeDcp770cw.E_44),
            ),
            BrokenComponent(component_type=ComponentTypeDcp770CW.TemperatureSensor),
        )
    )
    def overheating(self) -> None:
        print_fault_and_solution(
            "The internal temperature is too high.",
            "Unplug the device from the power socket and, "
            "if possible, lower the temperature of the room in which the device is located."
        )

    @Rule(
        OR(
            Error(code=ErrorCodeDcp770cw.E_46),
            BrokenComponent(component_type=ComponentTypeDcp770CW.WasteInkCartridge),
        )
    )
    def waste_ink(self) -> None:
        print_fault_and_solution(
            "The ink waste cartridge is too full.",
            "Contact Brother Customer Service using the 'Contact Us' section."
        )

    @Rule(
        OR(
            OR(
                Error(code=ErrorCodeDcp770cw.E_48),
                Error(code=ErrorCodeDcp770cw.E_4F),

            ),
            BrokenComponent(component_type=ComponentTypeDcp770CW.PrintHead),
        )
    )
    def print_head(self) -> None:
        print_fault_and_solution(
            "There is a problem with the print head.",
            "Contact Brother Customer Service using the 'Contact Us' section."
        )

    @Rule(
        OR(
            Error(code=ErrorCodeDcp770cw.E_49),
            BrokenComponent(component_type=ComponentTypeDcp770CW.TemperatureSensor),
        )
    )
    def temperature_too_low(self) -> None:
        print_fault_and_solution(
            "The internal temperature is too low.",
            "Unplug the device from the power socket and, "
            "if possible, increase the temperature of the room in which the device is located.."
        )

    @Rule(
        OR(
            OR(
                Error(code=ErrorCodeDcp770cw.E_50),
                Error(code=ErrorCodeDcp770cw.E_51),
                Error(code=ErrorCodeDcp770cw.E_52),
                Error(code=ErrorCodeDcp770cw.E_57),
                Error(code=ErrorCodeDcp770cw.E_5A),
                Error(code=ErrorCodeDcp770cw.E_5B),
                Error(code=ErrorCodeDcp770cw.E_5C),
                Error(code=ErrorCodeDcp770cw.E_5D),
                Error(code=ErrorCodeDcp770cw.E_5E),
            ),
            OR(
                BrokenComponent(component_type=ComponentTypeDcp770CW.PaperTray),
                BrokenComponent(component_type=ComponentTypeDcp770CW.PaperPositionSensor),
            ),
        )
    )
    def paper_jammed_or_position_sensor(self) -> None:
        print_fault_and_solution(
            "The machine does not operate due to a paper jam or a problem with the paper position sensor.",
            "Remove jammed sheet from paper tray"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeDcp770cw.E_8F),
            BrokenComponent(component_type=ComponentTypeDcp770CW.PaperTransportModule),
        )
    )
    def paper_transport_module_problem(self) -> None:
        print_fault_and_solution(
            "There was a problem with the paper transport module.",
            "Contact Brother Customer Service using the 'Contact Us' section."

        )

    @Rule(
        OR(
            OR(
                Error(code=ErrorCodeDcp770cw.E_A5),
                Error(code=ErrorCodeDcp770cw.E_A6),
                Error(code=ErrorCodeDcp770cw.E_A7),
                Error(code=ErrorCodeDcp770cw.E_A8),
                Error(code=ErrorCodeDcp770cw.E_AF),
            ),
            BrokenComponent(component_type=ComponentTypeDcp770CW.Scanner),
        )
    )
    def scanner(self) -> None:
        print_fault_and_solution(
            "There is a problem with the scanner.",
            "Contact Brother Customer Service using the 'Contact Us' section."
        )

    @Rule(
        OR(
            OR(
                Error(code=ErrorCodeDcp770cw.E_E2),
                Error(code=ErrorCodeDcp770cw.E_E3),
            ),
            BrokenComponent(component_type=ComponentTypeDcp770CW.PCB),
        )
    )
    def pcb(self) -> None:
        print_fault_and_solution(
            "There is a problem with the PCB.",
            "Contact Brother Customer Service using the 'Contact Us' section."
        )
