import json
from typing import Any, Dict, Mapping, Optional, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, Field

from classiq.interface.generator.generated_circuit_data import (
    FunctionDebugInfoInterface,
)
from classiq.interface.ide.visual_model import OperationLevel

ParameterValue = Union[float, int, str, None]


class FunctionDebugInfo(BaseModel):
    name: str
    # Parameters describe classical parameters passed to function
    # ParameterValue appears in type only for backwards compatibility
    parameters: Dict[str, str] = Field(type=Dict[str, ParameterValue])
    level: OperationLevel
    is_allocate_or_free: bool = Field(default=False)
    port_to_passed_variable_map: Dict[str, str] = Field(default_factory=dict)

    @staticmethod
    def param_controller(value: Any) -> str:
        try:
            return json.dumps(value)
        except TypeError:
            return repr(value)

    def update_map_from_port_mapping(self, port_mapping: Mapping[str, str]) -> None:
        new_port_to_passed_variable_map = self.port_to_passed_variable_map.copy()
        for old_key, new_key in port_mapping.items():
            if old_key in new_port_to_passed_variable_map:
                new_port_to_passed_variable_map[new_key] = (
                    new_port_to_passed_variable_map.pop(old_key)
                )
        self.port_to_passed_variable_map = new_port_to_passed_variable_map

    def update_map_from_inout_port_mapping(
        self, port_mapping: Mapping[str, Tuple[str, str]]
    ) -> None:
        new_port_to_passed_variable_map = self.port_to_passed_variable_map.copy()
        for old_key, (new_key1, new_key2) in port_mapping.items():
            if old_key in new_port_to_passed_variable_map:
                value = new_port_to_passed_variable_map.pop(old_key)
                new_port_to_passed_variable_map[new_key1] = value
                new_port_to_passed_variable_map[new_key2] = value
        self.port_to_passed_variable_map = new_port_to_passed_variable_map


class DebugInfoCollection(BaseModel):
    # Pydantic only started supporting UUID as keys in Pydantic V2
    # See https://github.com/pydantic/pydantic/issues/2096#issuecomment-814860206
    # For now, we use strings as keys in the raw data and use UUID in the wrapper logic
    data: Dict[str, FunctionDebugInfo] = Field(default_factory=dict)
    blackbox_data: Dict[str, FunctionDebugInfoInterface] = Field(default_factory=dict)

    def __setitem__(self, key: UUID, value: FunctionDebugInfo) -> None:
        self.data[str(key)] = value

    def get(self, key: UUID) -> Optional[FunctionDebugInfo]:
        return self.data.get(str(key))

    def __getitem__(self, key: UUID) -> FunctionDebugInfo:
        return self.data[str(key)]

    def __contains__(self, key: UUID) -> bool:
        return str(key) in self.data

    def get_blackbox_data(self, key: UUID) -> Optional[FunctionDebugInfoInterface]:
        if (debug_info := self.get(key)) is None:
            return None
        return self.blackbox_data.get(debug_info.name)
