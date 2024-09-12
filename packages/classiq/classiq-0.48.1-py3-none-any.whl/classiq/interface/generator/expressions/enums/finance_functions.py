from typing import Dict

from classiq.interface.generator.types.builtin_enum_declarations import (
    FinanceFunctionType,
)


def get_finance_function_dict() -> Dict[str, "FinanceFunctionType"]:
    return {
        "var": FinanceFunctionType.VAR,
        "expected shortfall": FinanceFunctionType.SHORTFALL,
        "x**2": FinanceFunctionType.X_SQUARE,
        "european call option": FinanceFunctionType.EUROPEAN_CALL_OPTION,
    }
