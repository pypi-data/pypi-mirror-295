from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Union, cast

import pydantic

from classiq.interface.ast_node import ASTNode
from classiq.interface.exceptions import ClassiqError
from classiq.interface.model.quantum_function_declaration import (
    AnonQuantumOperandDeclaration,
)

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock


class QuantumLambdaFunction(ASTNode):
    """
    The definition of an anonymous function passed as operand to higher-level functions
    """

    rename_params: Dict[str, str] = pydantic.Field(
        default_factory=dict,
        exclude=True,
    )

    pos_rename_params: List[str] = pydantic.Field(
        default_factory=list,
        description="Mapping of the declared param to the actual variable name used",
    )

    body: "StatementBlock" = pydantic.Field(
        description="A list of function calls passed to the operator"
    )

    _func_decl: Optional[AnonQuantumOperandDeclaration] = pydantic.PrivateAttr(
        default=None
    )

    _py_callable: Callable = pydantic.PrivateAttr(default=None)

    @property
    def py_callable(self) -> Callable:
        return self._py_callable

    def is_generative(self) -> bool:
        return self.py_callable is not None

    def set_py_callable(self, py_callable: Callable) -> None:
        self._py_callable = py_callable

    @property
    def func_decl(self) -> AnonQuantumOperandDeclaration:
        if self._func_decl is None:
            raise ClassiqError("Could not resolve lambda signature.")
        return self._func_decl

    def set_op_decl(self, fd: AnonQuantumOperandDeclaration) -> None:
        self._func_decl = fd

    def get_rename_params(self) -> List[str]:
        if self.pos_rename_params:
            return self.pos_rename_params
        return [
            self.rename_params.get(cast(str, param.name), cast(str, param.name))
            for param in self.func_decl.positional_arg_declarations
        ]


QuantumCallable = Union[str, QuantumLambdaFunction]
QuantumOperand = Union[QuantumCallable, List[QuantumCallable]]
