from facts.components import BrokenComponent, ComponentType
from facts.error_code import Error, ErrorCode
from knowledge import errors
from printer import Printer


def diagnose_problem(error_code: ErrorCode = None, component_type: ComponentType = None) -> None:
    engine = errors.PrinterProblemKnowledgeBase()
    engine.reset()
    engine.declare(Error(code=error_code), BrokenComponent(component_type=component_type))
    engine.run()


def diagnose_printer(printer: Printer) -> None:
    error_code = printer.get_error_code()
    broken_components = printer.get_broken_components()

    for broken_component in broken_components:
        diagnose_problem(error_code, broken_component)
