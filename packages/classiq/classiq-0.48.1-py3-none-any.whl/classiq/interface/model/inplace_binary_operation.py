from typing import Literal, Mapping, Sequence

from classiq.interface.enum_utils import StrEnum
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.handle_binding import ConcreteHandleBinding, HandleBinding
from classiq.interface.model.quantum_statement import HandleMetadata, QuantumOperation


class BinaryOperation(StrEnum):
    Addition = "inplace_add"
    Xor = "inplace_xor"


class InplaceBinaryOperation(QuantumOperation):
    kind: Literal["InplaceBinaryOperation"]

    target: ConcreteHandleBinding
    value: ConcreteHandleBinding
    operation: BinaryOperation

    @property
    def wiring_inouts(self) -> Mapping[str, HandleBinding]:
        return nameables_to_dict([self.target, self.value])

    @property
    def readable_inouts(self) -> Sequence[HandleMetadata]:
        suffix = f" of an in-place {self.operation.name.lower()} statement"
        return [
            HandleMetadata(
                handle=self.target, readable_location=f"as the target{suffix}"
            ),
            HandleMetadata(
                handle=self.value, readable_location=f"as the value{suffix}"
            ),
        ]
