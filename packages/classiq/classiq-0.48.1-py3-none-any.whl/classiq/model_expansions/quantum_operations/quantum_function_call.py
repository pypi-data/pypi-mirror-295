from classiq.interface.model.quantum_function_call import QuantumFunctionCall

from classiq.model_expansions.closure import FunctionClosure
from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.qmod.semantics.error_manager import ErrorManager


class QuantumFunctionCallEmitter(Emitter[QuantumFunctionCall]):
    def emit(self, call: QuantumFunctionCall, /) -> None:
        function = self._interpreter.evaluate(call.function).as_type(FunctionClosure)
        args = call.positional_args
        with ErrorManager().call(
            function.name
        ), function.scope.freeze(), self._propagated_var_stack.capture_variables(call):
            self._emit_quantum_function_call(function, args)
