from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalArray,
    ClassicalList,
    Estimation,
    Histogram,
    Integer,
    IQAERes,
    Real,
    StructMetaType,
    VQEResult,
)
from classiq.interface.generator.functions.type_name import Enum, TypeName
from classiq.interface.generator.types.qstruct_declaration import QStructDeclaration
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumNumeric,
    RegisterQuantumType,
)

ConcreteClassicalType = Annotated[
    Union[
        Integer,
        Real,
        Bool,
        ClassicalList,
        StructMetaType,
        TypeName,
        ClassicalArray,
        VQEResult,
        Histogram,
        Estimation,
        IQAERes,
    ],
    Field(discriminator="kind"),
]
ClassicalList.update_forward_refs(ConcreteClassicalType=ConcreteClassicalType)
ClassicalArray.update_forward_refs(ConcreteClassicalType=ConcreteClassicalType)

PythonClassicalTypes = (int, float, bool, list, Enum)

ConcreteQuantumType = Annotated[
    Union[QuantumBit, QuantumBitvector, QuantumNumeric, TypeName],
    Field(discriminator="kind", default_factory=QuantumBitvector),
]
QuantumBitvector.update_forward_refs(ConcreteQuantumType=ConcreteQuantumType)
TypeName.update_forward_refs(ConcreteQuantumType=ConcreteQuantumType)
QStructDeclaration.update_forward_refs(ConcreteQuantumType=ConcreteQuantumType)
RegisterQuantumType.update_forward_refs(ConcreteQuantumType=ConcreteQuantumType)
