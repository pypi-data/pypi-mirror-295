from typing import Any, Dict, List, Optional, Tuple

import pydantic

from classiq.interface.enum_utils import StrEnum
from classiq.interface.generator.hardware.hardware_data import SynthesisHardwareData
from classiq.interface.helpers.versioned_model import VersionedModel


class OperationLevel(StrEnum):
    QMOD_FUNCTION_CALL = "QMOD_CALL"
    QMOD_STATEMENT = "QMOD_STATEMENT"
    ENGINE_FUNCTION_CALL = "ENGINE_CALL"
    BASIS_GATE = "BASIS_GATE"
    UNKNOWN = "UNKNOWN"


class OperationType(StrEnum):
    REGULAR = "REGULAR"
    VAR_INITIALIZATION = "VAR_INITIALIZATION"
    BIND = "BIND"


class OperationData(pydantic.BaseModel):
    approximated_depth: Optional[int]
    width: int
    gate_count: Dict[str, int] = pydantic.Field(default_factory=dict)


class ProgramData(pydantic.BaseModel):
    hardware_data: SynthesisHardwareData


class OperationParameter(pydantic.BaseModel):
    label: str
    value: Optional[str]


class OperationLink(pydantic.BaseModel):
    label: str
    inner_label: Optional[str] = None
    qubits: Tuple[int, ...]
    type: str

    class Config:
        allow_mutation = False

    def __hash__(self) -> int:
        return hash((type(self), self.label, self.qubits, self.type))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, OperationLink):
            return False
        return hash(self) == hash(other)


class OperationLinks(pydantic.BaseModel):
    inputs: List[OperationLink]
    outputs: List[OperationLink]


class Operation(pydantic.BaseModel):
    name: str
    children: List["Operation"]
    operation_data: Optional[OperationData]
    operation_links: OperationLinks
    control_qubits: Tuple[int, ...] = pydantic.Field(default_factory=tuple)
    auxiliary_qubits: Tuple[int, ...]
    target_qubits: Tuple[int, ...]
    parameters: List[OperationParameter] = pydantic.Field(default_factory=list)
    operation_level: OperationLevel
    operation_type: OperationType = pydantic.Field(
        description="Identifies unique operations that are visualized differently"
    )


class ProgramVisualModel(VersionedModel):
    main_operation: Operation
    program_data: ProgramData
