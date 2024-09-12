from typing import Any, Dict, Literal, Mapping

import pydantic

from classiq.interface.exceptions import ClassiqInternalError, ClassiqValueError
from classiq.interface.generator.functions.concrete_types import ConcreteQuantumType
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator
from classiq.interface.model.parameter import Parameter


class AnonPortDeclaration(Parameter):
    kind: Literal["PortDeclaration"]

    quantum_type: ConcreteQuantumType
    direction: PortDeclarationDirection

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "PortDeclaration")

    @pydantic.validator("direction")
    def _direction_validator(
        cls, direction: PortDeclarationDirection, values: Mapping[str, Any]
    ) -> PortDeclarationDirection:
        if direction is PortDeclarationDirection.Output:
            quantum_type = values.get("quantum_type")
            if quantum_type is None:
                raise ClassiqValueError("Port declaration is missing a type")

        return direction

    def rename(self, new_name: str) -> "PortDeclaration":
        if type(self) not in (AnonPortDeclaration, PortDeclaration):
            raise ClassiqInternalError
        return PortDeclaration(**{**self.__dict__, "name": new_name})


class PortDeclaration(AnonPortDeclaration):
    name: str
