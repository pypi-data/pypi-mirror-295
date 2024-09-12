import ast
from abc import abstractmethod
from itertools import chain
from typing import TYPE_CHECKING, Dict, List, Tuple, TypeVar

import sympy

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.type_name import TypeName
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.handle_binding import (
    FieldHandleBinding,
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumExpressionOperation,
)
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumNumeric,
)
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import QuantumSymbol
from classiq.model_expansions.sympy_conversion.sympy_to_python import (
    translate_sympy_quantum_expression,
)
from classiq.model_expansions.visitors.variable_references import VarRefCollector

ExpressionOperationT = TypeVar("ExpressionOperationT", bound=QuantumExpressionOperation)


class ExpressionOperationEmitter(Emitter[ExpressionOperationT]):
    @abstractmethod
    def emit(self, op: ExpressionOperationT, /) -> None:
        pass

    def _emit_with_split(
        self,
        op: ExpressionOperationT,
        expression: Expression,
        symbols_to_split: List[QuantumSymbol],
    ) -> None:
        symbols_parts, bind_ops = self._get_bind_ops(symbols_to_split)

        for symbol_parts in symbols_parts:
            for symbol, symbol_part_var_name in symbol_parts:
                if symbol.handle.identifier not in self._current_scope:
                    self._interpreter.emit_statement(
                        VariableDeclarationStatement(
                            name=symbol_part_var_name,
                            quantum_type=symbol.quantum_type,
                        )
                    )

        new_expression = self._update_op_expression(
            {
                symbol.handle: symbol_part_var_name
                for symbol, symbol_part_var_name in chain.from_iterable(symbols_parts)
            },
            expression,
        )
        new_op = op.copy(update=dict(expression=new_expression))

        self._interpreter.emit_statement(
            WithinApply(
                compute=bind_ops,
                action=[new_op],
                source_ref=op.source_ref,
            )
        )

    def _update_op_expression(
        self,
        symbol_parts: Dict[HandleBinding, str],
        expression: Expression,
    ) -> Expression:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(expression.expr))

        new_expr_str = expression.expr
        for handle in vrc.var_handles:
            collapsed_handle = handle.collapse()
            if collapsed_handle in symbol_parts:
                new_expr_str = new_expr_str.replace(
                    str(handle), symbol_parts[collapsed_handle]
                )
        self._check_all_handles_were_replaced(new_expr_str)

        new_expr = Expression(expr=new_expr_str)
        new_expr._evaluated_expr = EvaluatedExpression(
            value=self._interpreter.evaluate(new_expr).value
        )
        return new_expr

    @staticmethod
    def _check_all_handles_were_replaced(new_expr_str: str) -> None:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(new_expr_str))
        for handle in vrc.var_handles:
            if isinstance(
                handle,
                (SubscriptHandleBinding, SlicedHandleBinding, FieldHandleBinding),
            ):
                raise ClassiqInternalExpansionError(f"Did not replace handle {handle}")

    def _get_bind_ops(
        self,
        symbols_to_split: List[QuantumSymbol],
    ) -> Tuple[List[List[Tuple[QuantumSymbol, str]]], List[BindOperation]]:
        bind_ops = []
        symbols_parts = []
        for symbol in symbols_to_split:
            symbol_parts = self._get_symbol_parts(symbol)
            symbols_parts.append(symbol_parts)
            bind_ops.append(
                BindOperation(
                    in_handles=[symbol.handle],
                    out_handles=[
                        HandleBinding(name=symbol_part_var_name)
                        for _, symbol_part_var_name in symbol_parts
                    ],
                )
            )
        return symbols_parts, bind_ops

    def _get_symbol_parts(
        self, symbol: QuantumSymbol
    ) -> List[Tuple[QuantumSymbol, str]]:
        quantum_type = symbol.quantum_type

        if isinstance(quantum_type, (QuantumBit, QuantumNumeric)):
            return [
                (
                    symbol,
                    self._counted_name_allocator.allocate(symbol.handle.identifier),
                )
            ]

        if isinstance(quantum_type, QuantumBitvector):
            if not quantum_type.has_length:
                raise ClassiqExpansionError(
                    f"Could not determine the length of quantum array "
                    f"{symbol.handle}."
                )
            return list(
                chain.from_iterable(
                    self._get_symbol_parts(symbol[idx])
                    for idx in range(quantum_type.length_value)
                )
            )

        if TYPE_CHECKING:
            assert isinstance(quantum_type, TypeName)

        return list(
            chain.from_iterable(
                self._get_symbol_parts(field_symbol)
                for field_symbol in symbol.fields.values()
            )
        )

    def _get_symbols_to_split(self, expression: Expression) -> List[QuantumSymbol]:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(expression.expr))
        symbol_names_to_split = dict.fromkeys(
            handle.name
            for handle in vrc.var_handles
            if isinstance(handle, (SubscriptHandleBinding, FieldHandleBinding))
        )
        return [
            symbol
            for symbol_name in symbol_names_to_split
            if isinstance(
                symbol := self._current_scope[symbol_name].value,
                QuantumSymbol,
            )
        ]

    def _evaluate_op_expression(self, op: ExpressionOperationT) -> Expression:
        return self._evaluate_expression(op.expression)

    def _evaluate_expression(self, expression: Expression) -> Expression:
        evaluated_expression = self._interpreter.evaluate(expression)
        if isinstance(evaluated_expression.value, sympy.Basic):
            new_expression = Expression(
                expr=translate_sympy_quantum_expression(evaluated_expression.value)
            )
        else:
            new_expression = Expression(expr=str(evaluated_expression.value))
        new_expression._evaluated_expr = EvaluatedExpression(
            value=evaluated_expression.value
        )
        return new_expression

    def _evaluate_types_in_expression(
        self, op: ExpressionOperationT, expression: Expression
    ) -> ExpressionOperationT:
        op_with_evaluated_types = op.copy(update={"expression": expression})
        vrc = VarRefCollector()
        vrc.visit(ast.parse(op_with_evaluated_types.expression.expr))
        handles = vrc.var_handles
        op_with_evaluated_types.set_var_handles(handles)
        op_with_evaluated_types.initialize_var_types(
            {
                handle.name: self._interpreter.evaluate(handle)
                .as_type(QuantumSymbol)
                .quantum_type
                for handle in handles
            },
            self._machine_precision,
        )
        return op_with_evaluated_types
