from facts.components import get_all_component_types, ComponentType
from facts.error_code import ErrorCode
from printer import Printer
from printer_diagnoser import diagnose_printer


def working_printer() -> None:
    diagnose_printer(Printer(get_all_component_types()))


def broken_printer() -> None:
    printer = Printer(get_all_component_types())
    printer.break_component(ComponentType.FrontCassette)
    diagnose_printer(printer)


def error_printer() -> None:
    printer = Printer(get_all_component_types())
    printer.set_error_code(ErrorCode.E_5C02)
    diagnose_printer(printer)


if __name__ == '__main__':
    working_printer()
    broken_printer()
    error_printer()
