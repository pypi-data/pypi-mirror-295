from typing import TYPE_CHECKING, List, Tuple

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.inplace_binary_operation import (
    BinaryOperation,
    InplaceBinaryOperation,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumStatement
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumNumeric,
)
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.model_expansions.closure import FunctionClosure
from classiq.model_expansions.evaluators.parameter_types import (
    evaluate_types_in_quantum_symbols,
)
from classiq.model_expansions.evaluators.quantum_type_utils import (
    validate_inplace_binary_op_vars,
)
from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import QuantumSymbol, Scope
from classiq.qmod.builtins.functions import CX, allocate, integer_xor, modular_add


def _binary_function_declaration(
    op: BinaryOperation,
) -> NamedParamsQuantumFunctionDeclaration:
    return {
        BinaryOperation.Addition: modular_add.func_decl,
        BinaryOperation.Xor: integer_xor.func_decl,
    }[op]


class InplaceBinaryOperationEmitter(Emitter[InplaceBinaryOperation]):
    def emit(self, op: InplaceBinaryOperation, /) -> None:
        value_var = self._interpreter.evaluate(op.value).as_type(QuantumSymbol)
        target_var = self._interpreter.evaluate(op.target).as_type(QuantumSymbol)
        value_var, target_var = evaluate_types_in_quantum_symbols(
            [value_var, target_var], self._current_scope
        )
        validate_inplace_binary_op_vars(value_var, target_var, op.operation.value)
        if TYPE_CHECKING:
            assert isinstance(value_var.quantum_type, QuantumNumeric)
            assert isinstance(target_var.quantum_type, QuantumNumeric)

        frac_digits_diff = (
            value_var.quantum_type.fraction_digits_value
            - target_var.quantum_type.fraction_digits_value
        )
        if (
            frac_digits_diff == value_var.quantum_type.size_in_bits
            or -frac_digits_diff == target_var.quantum_type.size_in_bits
        ):
            with self._propagated_var_stack.capture_variables(op):
                return

        value_var = QuantumSymbol(
            handle=HandleBinding(name="value"), quantum_type=value_var.quantum_type
        )
        target_var = QuantumSymbol(
            handle=HandleBinding(name="target"),
            quantum_type=target_var.quantum_type,
        )
        inplace_binary_op_function = FunctionClosure.create(
            name=op.operation.value,
            positional_arg_declarations=[
                PortDeclaration(
                    name=value_var.handle.name,
                    quantum_type=value_var.quantum_type,
                    direction=PortDeclarationDirection.Inout,
                ),
                PortDeclaration(
                    name=target_var.handle.name,
                    quantum_type=target_var.quantum_type,
                    direction=PortDeclarationDirection.Inout,
                ),
            ],
            body=_build_inplace_binary_operation(
                value_var=value_var,
                target_var=target_var,
                internal_function_declaration=_binary_function_declaration(
                    op.operation
                ),
            ),
            scope=Scope(parent=self._current_scope),
        )
        with self._propagated_var_stack.capture_variables(op):
            self._emit_quantum_function_call(
                inplace_binary_op_function, [op.value, op.target]
            )


def _build_inplace_binary_operation(
    value_var: QuantumSymbol,
    target_var: QuantumSymbol,
    internal_function_declaration: NamedParamsQuantumFunctionDeclaration,
) -> List[QuantumStatement]:
    if TYPE_CHECKING:
        assert isinstance(value_var.quantum_type, QuantumNumeric)
        assert isinstance(target_var.quantum_type, QuantumNumeric)

    frac_digits_diff = (
        value_var.quantum_type.fraction_digits_value
        - target_var.quantum_type.fraction_digits_value
    )
    size_diff = (
        value_var.quantum_type.size_in_bits - target_var.quantum_type.size_in_bits
    )

    target_overlap_var, target_var_decls, target_bind_ops = (
        _trim_superfluous_fraction_digits("target", target_var, -frac_digits_diff)
    )
    value_overlap_var, value_trim_var_decls, value_bind_ops = (
        _trim_superfluous_fraction_digits("value", value_var, frac_digits_diff)
    )
    (
        value_padded_var,
        value_pad_var_decls,
        value_pad_pre_bind_ops,
        value_pad_init_ops,
        value_post_bind_ops,
    ) = _pad_with_sign_bit("value", value_overlap_var, size_diff)

    op_call = _internal_inplace_binary_operation_function_call(
        internal_function_declaration,
        value_padded_var.handle,
        target_overlap_var.handle,
    )

    return [
        *target_var_decls,
        *value_trim_var_decls,
        *value_pad_var_decls,
        WithinApply(
            compute=[
                *target_bind_ops,
                *value_bind_ops,
                *value_pad_pre_bind_ops,
                *value_pad_init_ops,
                *value_post_bind_ops,
            ],
            action=[
                op_call,
            ],
        ),
    ]


def _internal_inplace_binary_operation_function_call(
    internal_function_declaration: NamedParamsQuantumFunctionDeclaration,
    value_var: HandleBinding,
    target_var: HandleBinding,
) -> QuantumFunctionCall:
    internal_function_call = QuantumFunctionCall(
        function=internal_function_declaration.name,
        positional_args=[value_var, target_var],
    )
    internal_function_call.set_func_decl(internal_function_declaration)
    return internal_function_call


def _trim_superfluous_fraction_digits(
    kind: str, var: QuantumSymbol, frac_digits_diff: int
) -> Tuple[QuantumSymbol, List[VariableDeclarationStatement], List[BindOperation]]:
    if frac_digits_diff <= 0:
        return var, [], []

    quantum_type = var.quantum_type
    if TYPE_CHECKING:
        assert isinstance(quantum_type, QuantumNumeric)

    trimmed_fraction_digits_var = QuantumSymbol(
        handle=HandleBinding(name=f"trimmed_{kind}_fraction_digits"),
        quantum_type=QuantumBitvector(
            length=Expression(expr=str(frac_digits_diff)),
        ),
    )
    overlap_var = QuantumSymbol(
        handle=HandleBinding(name=f"{kind}_overlap"),
        quantum_type=QuantumNumeric(
            size=Expression(expr=str(quantum_type.size_in_bits - frac_digits_diff)),
            is_signed=quantum_type.is_signed,
            fraction_digits=Expression(expr="0"),
        ),
    )
    bind_targets = trimmed_fraction_digits_var, overlap_var

    split_var_declarations = [
        VariableDeclarationStatement(
            name=var.handle.name,
            quantum_type=var.quantum_type,
        )
        for var in bind_targets
    ]
    bind_op = BindOperation(
        in_handles=[var.handle],
        out_handles=[var.handle for var in bind_targets],
    )

    return overlap_var, split_var_declarations, [bind_op]


def _pad_with_sign_bit(kind: str, var: QuantumSymbol, size_diff: int) -> Tuple[
    QuantumSymbol,
    List[VariableDeclarationStatement],
    List[QuantumStatement],
    List[QuantumFunctionCall],
    List[BindOperation],
]:
    quantum_type = var.quantum_type
    if TYPE_CHECKING:
        assert isinstance(quantum_type, QuantumNumeric)

    if not quantum_type.sign_value or size_diff >= 0:
        return var, [], [], [], []

    significand_var, sign_var, sign_split_bind = _split_sign(kind, var)
    padding_var, padding_allocation = _allocate_padding(kind, size_diff)
    padding_init_ops = _init_padding(sign_var, padding_var, size_diff)

    padded_var = QuantumSymbol(
        handle=HandleBinding(name=f"padded_{kind}"),
        quantum_type=QuantumNumeric(
            size=Expression(expr=str(quantum_type.size_in_bits - size_diff)),
            is_signed=Expression(expr="False"),
            fraction_digits=Expression(expr="0"),
        ),
    )
    padding_rebind = BindOperation(
        in_handles=[significand_var.handle, sign_var.handle, padding_var.handle],
        out_handles=[padded_var.handle],
    )

    var_decls = [
        VariableDeclarationStatement(
            name=var.handle.name,
            quantum_type=var.quantum_type,
        )
        for var in (significand_var, sign_var, padding_var, padded_var)
    ]

    return (
        padded_var,
        var_decls,
        [sign_split_bind, padding_allocation],
        padding_init_ops,
        [padding_rebind],
    )


def _init_padding(
    sign_var: QuantumSymbol, padding_var: QuantumSymbol, size_diff: int
) -> List[QuantumFunctionCall]:
    padding_init_ops = [
        QuantumFunctionCall(
            function=CX.func_decl.name,
            positional_args=[sign_var.handle, padding_var[idx].handle],
        )
        for idx in range(-size_diff)
    ]
    for cx_call in padding_init_ops:
        cx_call.set_func_decl(CX.func_decl)
    return padding_init_ops


def _allocate_padding(
    kind: str, size_diff: int
) -> Tuple[QuantumSymbol, QuantumFunctionCall]:
    padding_var = QuantumSymbol(
        handle=HandleBinding(name=f"{kind}_sign_padding"),
        quantum_type=QuantumBitvector(
            length=Expression(expr=str(-size_diff)),
        ),
    )
    padding_allocation = QuantumFunctionCall(
        function=allocate.func_decl.name,
        positional_args=[Expression(expr=str(-size_diff)), padding_var.handle],
    )
    padding_allocation.set_func_decl(allocate.func_decl)
    return padding_var, padding_allocation


def _split_sign(
    kind: str, var: QuantumSymbol
) -> Tuple[QuantumSymbol, QuantumSymbol, BindOperation]:
    significand_var = QuantumSymbol(
        handle=HandleBinding(name=f"{kind}_significand"),
        quantum_type=QuantumNumeric(
            size=Expression(expr=str(var.quantum_type.size_in_bits - 1)),
            is_signed=Expression(expr="False"),
            fraction_digits=Expression(expr="0"),
        ),
    )
    sign_var = QuantumSymbol(
        handle=HandleBinding(name=f"{kind}_sign_bit"),
        quantum_type=QuantumBit(),
    )
    sign_split_bind = BindOperation(
        in_handles=[var.handle],
        out_handles=[significand_var.handle, sign_var.handle],
    )
    return significand_var, sign_var, sign_split_bind
