from facts.components import ComponentTypeG6000, ComponentType, ComponentTypeDcp770CW
from facts.error_code import ErrorCodeG6000, ErrorCode, ErrorCodeDcp770cw
from printers.BrotherDcp770Dw import BrotherDcp770Dw
from printers.CannonG6000 import CannonG6000
from printer_diagnoser import diagnose_printer
from printers.Printer import Printer


def working_printer(printer: Printer) -> None:
    diagnose_printer(printer)


def broken_printer(printer: Printer, broken_component: ComponentType) -> None:
    printer.break_component(broken_component)
    diagnose_printer(printer)


def error_printer(printer: Printer, error_code: ErrorCode) -> None:
    printer.set_error_code(error_code)
    diagnose_printer(printer)


def cannon_printer() -> None:
    error_code = ErrorCodeG6000.E_5C02
    broken_component = ComponentTypeG6000.BacksidePaperTray

    working_printer(CannonG6000())
    broken_printer(CannonG6000(), broken_component)
    error_printer(CannonG6000(), error_code)


def brother_printer() -> None:
    error_code = ErrorCodeDcp770cw.E_3F
    broken_component = ComponentTypeDcp770CW.PCB

    working_printer(BrotherDcp770Dw())
    broken_printer(BrotherDcp770Dw(), broken_component)
    error_printer(BrotherDcp770Dw(), error_code)


if __name__ == "__main__":
    # cannon_printer()
    brother_printer()
