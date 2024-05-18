from experta import KnowledgeEngine

from facts.components import BrokenComponent, ComponentType
from facts.error_code import Error, ErrorCode
from printers.Printer import Printer


def diagnose_problem(
        engine: KnowledgeEngine,
        error_code: ErrorCode = None,
        component_type: ComponentType = None,
) -> None:
    engine.reset()
    engine.declare(Error(code=error_code), BrokenComponent(component_type=component_type))
    engine.run()


def diagnose_printer(printer: Printer) -> None:
    print(printer)

    error_code = printer.get_error_code()
    broken_components = printer.get_broken_components()
    if len(broken_components) <= 0:
        diagnose_problem(printer.get_knowledge_engine(), error_code)

    for broken_component in broken_components:
        diagnose_problem(printer.get_knowledge_engine(), error_code, broken_component)

    print()
