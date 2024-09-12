import logging
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

import pydantic
from typing_extensions import TypeAlias

from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.register_role import RegisterRole
from classiq.interface.generator.synthesis_metadata.synthesis_execution_data import (
    ExecutionData,
)
from classiq.interface.ide.visual_model import OperationParameter

_logger = logging.getLogger(__name__)
ParameterName = str
IOQubitMapping: TypeAlias = Dict[str, Tuple[int, ...]]

CLASSIQ_HIERARCHY_SEPARATOR: Literal["."] = "."

VISUALIZATION_HIDE_LIST = [
    "apply_to_all",
    "repeat",
    "control",
    "mcx",
    "iteration",
    "stmt_block",
]


def last_name_in_call_hierarchy(name: str) -> str:
    return name.split(CLASSIQ_HIERARCHY_SEPARATOR)[-1]


class QubitMapping(pydantic.BaseModel):
    logical_inputs: IOQubitMapping = pydantic.Field(default_factory=dict)
    logical_outputs: IOQubitMapping = pydantic.Field(default_factory=dict)
    physical_inputs: IOQubitMapping = pydantic.Field(default_factory=dict)
    physical_outputs: IOQubitMapping = pydantic.Field(default_factory=dict)


class GeneratedRegister(pydantic.BaseModel):
    name: str
    role: RegisterRole
    qubit_indexes_relative: List[int]
    qubit_indexes_absolute: List[int]

    def __len__(self) -> int:
        return self.qubit_indexes_relative.__len__()

    @property
    def width(self) -> int:
        return len(self)


class GeneratedFunction(pydantic.BaseModel):
    name: str
    control_states: List[ControlState]
    registers: List[GeneratedRegister] = list()
    depth: Optional[int]
    width: Optional[int]
    released_auxiliary_qubits: List[int] = list()
    dangling_inputs: Dict[str, GeneratedRegister] = dict()
    dangling_outputs: Dict[str, GeneratedRegister] = dict()

    def __getitem__(self, key: Union[int, str]) -> GeneratedRegister:
        if isinstance(key, int):
            return self.registers[key]
        if isinstance(key, str):
            for register in self.registers:
                if key == register.name:
                    return register
        raise KeyError(key)

    def get(self, key: Union[int, str]) -> Optional[GeneratedRegister]:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    @property
    def should_appear_in_visualization(self) -> bool:
        return all(
            hide_regex not in last_name_in_call_hierarchy(self.name.lower())
            for hide_regex in VISUALIZATION_HIDE_LIST
        )


class GeneratedCircuitData(pydantic.BaseModel):
    width: int
    circuit_parameters: List[ParameterName] = pydantic.Field(default_factory=list)
    qubit_mapping: QubitMapping = pydantic.Field(default_factory=QubitMapping)
    execution_data: Optional[ExecutionData] = pydantic.Field(default=None)

    @classmethod
    def from_empty_logic_flow(cls) -> "GeneratedCircuitData":
        return cls(width=0)


class FunctionDebugInfoInterface(pydantic.BaseModel):
    generated_function: Optional[GeneratedFunction]
    children: List["FunctionDebugInfoInterface"]
    relative_qubits: Tuple[int, ...]
    absolute_qubits: Optional[Tuple[int, ...]]
    is_basis_gate: Optional[bool]
    parameters: List[OperationParameter] = list()
    port_to_passed_variable_map: Dict[str, str] = pydantic.Field(default_factory=dict)

    @property
    def registers(self) -> List[GeneratedRegister]:
        if self.generated_function is None:
            return list()
        return self.generated_function.registers

    @property
    def is_controlled(self) -> bool:
        if self.generated_function is None:
            return False
        return len(self.generated_function.control_states) > 0

    @property
    def control_states(self) -> List[ControlState]:
        if self.generated_function is None:
            return list()
        return self.generated_function.control_states

    @staticmethod
    def create_parameters_from_dict(
        parameters: Dict[str, str]
    ) -> List[OperationParameter]:
        return [
            OperationParameter(label=key, value=value)
            for key, value in parameters.items()
        ]

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def propagate_absolute_qubits(self) -> None:
        if self.absolute_qubits is None:
            return

        for register in self.registers:
            register.qubit_indexes_absolute = list(
                _get_absolute_from_relative(
                    self.absolute_qubits, tuple(register.qubit_indexes_relative)
                )
            )

        for child in self.children:
            child.absolute_qubits = _get_absolute_from_relative(
                self.absolute_qubits, child.relative_qubits
            )
            child.propagate_absolute_qubits()


def _get_absolute_from_relative(
    absolute_qubits: Tuple[int, ...], relative_qubits: Tuple[int, ...]
) -> Tuple[int, ...]:
    if max(relative_qubits) >= len(absolute_qubits):
        _logger.warning(
            "Invalid qubit computation (relative qubits: %s, absolute qubits: %s)",
            relative_qubits,
            absolute_qubits,
        )
        return tuple()
    return tuple(absolute_qubits[relative_qubit] for relative_qubit in relative_qubits)
