from experta import KnowledgeEngine, Rule, OR, AND

from facts.components import ComponentTypeG6000, BrokenComponent
from facts.error_code import ErrorCodeG6000, Error
from knowledge.utils import print_fault_and_solution


class CannonG6000ProblemKnowledgeBase(KnowledgeEngine):

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1300),
            BrokenComponent(component_type=ComponentTypeG6000.BacksidePaperTray)
        )
    )
    def paper_jammed_on_fetching_from_backside_tray(self) -> None:
        print_fault_and_solution("Paper jammed", "Remove jammed sheet from backside tray")

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1303),
            BrokenComponent(component_type=ComponentTypeG6000.FrontCassette)
        )
    )
    def paper_jammed_on_fetching_from_cassette_tray(self) -> None:
        print_fault_and_solution("Paper jammed", "Remove jammed sheet from front side cassette")

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1304),
            BrokenComponent(component_type=ComponentTypeG6000.AnyPaperTray)
        )
    )
    def paper_jammed_on_doublesided_print(self) -> None:
        print_fault_and_solution(
            "Paper jammed on doublesided print",
            "Remove jammed sheet from the printing mechanism"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1313),
            BrokenComponent(component_type=ComponentTypeG6000.PrintingMechanism)
        )
    )
    def paper_jammed_on_already_printed_paper(self) -> None:
        print_fault_and_solution(
            "Already printed paper jammed",
            "Remove jammed sheet from the top of the printing mechanism"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1365),
            BrokenComponent(component_type=ComponentTypeG6000.InkCartridge)
        )
    )
    def ink_cartridge_open(self) -> None:
        print_fault_and_solution(
            "Ink cartridge open",
            "Close all open cartridge valves before continuing to replace the print head"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1366),
            BrokenComponent(component_type=ComponentTypeG6000.InkCartridge)
        )
    )
    def ink_cartridge_closed(self) -> None:
        print_fault_and_solution(
            "Ink cartridge closed",
            "Open all closed cartridge valves before continuing with printing"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1367),
            BrokenComponent(component_type=ComponentTypeG6000.InkCartridge)
        )
    )
    def not_enough_ink_to_flush(self) -> None:
        print_fault_and_solution("Not enough ink to flush", "Add missing ink")

    @Rule(
        OR(
            OR(
                Error(code=ErrorCodeG6000.E_1431),
                Error(code=ErrorCodeG6000.E_1432),
                Error(code=ErrorCodeG6000.E_1471),
                Error(code=ErrorCodeG6000.E_1472),
                Error(code=ErrorCodeG6000.E_1473),
            ),
            BrokenComponent(component_type=ComponentTypeG6000.PrintHead)
        )
    )
    def print_head_not_recognized(self) -> None:
        print_fault_and_solution(
            "Print head not recognized",
            "Print head might be corrupted or counterfeit. Replace with correct print head"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1470),
            BrokenComponent(component_type=ComponentTypeG6000.PrintHead)
        )
    )
    def print_head_inserted_incorrectly(self) -> None:
        print_fault_and_solution("Print head inserted incorrectly", "Reseat the print head")

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1476),
            BrokenComponent(component_type=ComponentTypeG6000.PrintHead)
        )
    )
    def incorrect_print_head(self) -> None:
        print_fault_and_solution(
            "Incorrect pint head",
            "Check if your print head model is supported by the printer"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1641),
            BrokenComponent(component_type=ComponentTypeG6000.InkCartridge)
        )
    )
    def low_ink_level(self) -> None:
        print_fault_and_solution(
            "Low ink level",
            "The level of remaining ink in one of the ink tanks "
            "may have equaled the lower limit line shown on the ink tank."
            "Add ink"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1642),
            BrokenComponent(component_type=ComponentTypeG6000.InkCartridge)
        )
    )
    def not_enough_ink(self) -> None:
        print_fault_and_solution(
            "Not enough ink to print",
            "The amount of ink might not be enough to print. Add ink"
        )

    @Rule(
        OR(
            OR(
                Error(code=ErrorCodeG6000.E_1700),
                Error(code=ErrorCodeG6000.E_1701),
            ), BrokenComponent(component_type=ComponentTypeG6000.WasteInkContainer)
        )
    )
    def waste_ink_container_almost_full(self) -> None:
        print_fault_and_solution("Waste ink container is amost full", "Empty it before continuing")

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_1890),
            BrokenComponent(component_type=ComponentTypeG6000.PrintHeadHolder)
        )
    )
    def print_head_holder_covered(self) -> None:
        print_fault_and_solution(
            "Print head holder covered",
            "It may be covered with residual protective film. "
            "Remove the film before continuing"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_2500),
            BrokenComponent(component_type=ComponentTypeG6000.PrintHead)
        )
    )
    def automatic_print_head_alignment_not_working_correctly(self) -> None:
        print(
            "The cause of the following problem may be that "
            "the automatic print head alignment function is not working properly."
            "The problem might be caused by:"
            "the print head nozzles are clogged, "
            "paper other than A4 or Letter size is loaded in the cassette,"
            "the paper exit hole is exposed to a strong light source."
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_5011),
            Error(code=ErrorCodeG6000.E_5012),
            Error(code=ErrorCodeG6000.E_5050),
            Error(code=ErrorCodeG6000.E_5205),
            Error(code=ErrorCodeG6000.E_5206),
            Error(code=ErrorCodeG6000.E_5400),
            Error(code=ErrorCodeG6000.E_5700),
            Error(code=ErrorCodeG6000.E_5C02),
            Error(code=ErrorCodeG6000.E_6001),
            Error(code=ErrorCodeG6000.E_6004),
            Error(code=ErrorCodeG6000.E_6500),
            Error(code=ErrorCodeG6000.E_6800),
            Error(code=ErrorCodeG6000.E_6801),
            Error(code=ErrorCodeG6000.E_6830),
            Error(code=ErrorCodeG6000.E_6831),
            Error(code=ErrorCodeG6000.E_6832),
            Error(code=ErrorCodeG6000.E_6833),
            Error(code=ErrorCodeG6000.E_6900),
            Error(code=ErrorCodeG6000.E_6901),
            Error(code=ErrorCodeG6000.E_6902),
            Error(code=ErrorCodeG6000.E_6910),
            Error(code=ErrorCodeG6000.E_6911),
            Error(code=ErrorCodeG6000.E_6920),
            Error(code=ErrorCodeG6000.E_6921),
            Error(code=ErrorCodeG6000.E_6930),
            Error(code=ErrorCodeG6000.E_6931),
            Error(code=ErrorCodeG6000.E_6932),
            Error(code=ErrorCodeG6000.E_6933),
            Error(code=ErrorCodeG6000.E_6936),
            Error(code=ErrorCodeG6000.E_6937),
            Error(code=ErrorCodeG6000.E_6938),
            Error(code=ErrorCodeG6000.E_6940),
            Error(code=ErrorCodeG6000.E_6941),
            Error(code=ErrorCodeG6000.E_6942),
            Error(code=ErrorCodeG6000.E_6943),
            Error(code=ErrorCodeG6000.E_6944),
            Error(code=ErrorCodeG6000.E_6945),
            Error(code=ErrorCodeG6000.E_6946),
            Error(code=ErrorCodeG6000.E_6D01),
            Error(code=ErrorCodeG6000.E_C000),
        )
    )
    def printer_error(self) -> None:
        print_fault_and_solution(
            "Printer error",
            "Unplug and replug the printer. If that doesn't help contact the manufacturer"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_5100),
            BrokenComponent(component_type=ComponentTypeG6000.PrintHead)
        )
    )
    def printer_error_print_head(self) -> None:
        print_fault_and_solution(
            "Printer error",
            "Cancel current print by pressing Stop OR turn the printer off. "
            "Check print head movement OR remove any obstructions. Turn on the printer."
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_5200),
            BrokenComponent(component_type=ComponentTypeG6000.InkCartridge)
        )
    )
    def printer_error_ink(self) -> None:
        print_fault_and_solution("Printer error", "Add ink if necessary")

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_5B00),
            Error(code=ErrorCodeG6000.E_5B01),
        )
    )
    def printer_error_critical(self) -> None:
        print_fault_and_solution("Printer error", "Contact the manufacturer")

    @Rule(Error(code=ErrorCodeG6000.E_6000))
    def printer_error_paper_jam(self) -> None:
        print_fault_and_solution(
            "Printer error",
            "Remove paper jam OR unplug and replug the printer. "
            "If that doesn't help contact the manufacture"
        )

    @Rule(
        OR(
            OR(
                Error(code=ErrorCodeG6000.E_6A80),
                Error(code=ErrorCodeG6000.E_6A81),
            ),
            BrokenComponent(component_type=ComponentTypeG6000.PaperTransportModule)
        )
    )
    def printer_error_transport_module(self) -> None:
        print_fault_and_solution(
            "Printer error",
            "Paper may be jammed in the paper transport module. "
            "Remove jammed sheet from front side cassette."
            "If that doesn't help contact the manufacture"
        )

    @Rule(
        OR(
            Error(code=ErrorCodeG6000.E_7500),
            Error(code=ErrorCodeG6000.E_7600),
            Error(code=ErrorCodeG6000.E_7700),
            Error(code=ErrorCodeG6000.E_7800),
        )
    )
    def printer_error_require_repair(self) -> None:
        print_fault_and_solution(
            "Printer error requiring repair",
            "Unplug the printer and contact the manufacturer"
        )

    @Rule(
        AND(
            Error(code=None),
            BrokenComponent(component_type=None)
        )
    )
    def undefined_problem(self) -> None:
        print("Everything works fine!")
