from collections import Counter
from typing import List, Literal, Mapping, NewType

import pydantic

from classiq.interface.ast_node import ASTNode
from classiq.interface.debug_info.debug_info import DebugInfoCollection
from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.constant import Constant
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.generator.quantum_function_call import SUFFIX_RANDOMIZER
from classiq.interface.generator.types.enum_declaration import EnumDeclaration
from classiq.interface.generator.types.qstruct_declaration import QStructDeclaration
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.helpers.versioned_model import VersionedModel
from classiq.interface.model.native_function_definition import (
    NativeFunctionDefinition,
)
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)
from classiq.interface.model.statement_block import StatementBlock

USER_MODEL_MARKER = "user"

MAIN_FUNCTION_NAME = "main"
CLASSICAL_ENTRY_FUNCTION_NAME = "cmain"

DEFAULT_PORT_SIZE = 1

SerializedModel = NewType("SerializedModel", str)

TYPE_NAME_CONFLICT_BUILTIN = (
    "Type '{name}' conflicts with a builtin type with the same name"
)

TYPE_NAME_CONFLICT_USER = (
    "Type '{name}' conflicts with a previously defined type with the same name"
)


def _create_empty_main_function() -> NativeFunctionDefinition:
    return NativeFunctionDefinition(name=MAIN_FUNCTION_NAME)


class VersionedSerializedModel(VersionedModel):
    model: SerializedModel


class Model(VersionedModel, ASTNode):

    kind: Literal["user"] = pydantic.Field(default=USER_MODEL_MARKER)

    # Must be validated before logic_flow
    functions: List[NativeFunctionDefinition] = pydantic.Field(
        default_factory=list,
        description="The user-defined custom type library.",
    )

    enums: List[EnumDeclaration] = pydantic.Field(
        default_factory=list,
        description="user-defined enums",
    )

    types: List[StructDeclaration] = pydantic.Field(
        default_factory=list,
        description="user-defined structs",
    )

    qstructs: List[QStructDeclaration] = pydantic.Field(
        default_factory=list,
        description="user-defined quantum structs",
    )

    classical_execution_code: str = pydantic.Field(
        description="The classical execution code of the model", default=""
    )

    constants: List[Constant] = pydantic.Field(
        default_factory=list,
    )

    constraints: Constraints = pydantic.Field(default_factory=Constraints)

    execution_preferences: ExecutionPreferences = pydantic.Field(
        default_factory=ExecutionPreferences
    )
    preferences: Preferences = pydantic.Field(default_factory=Preferences)

    debug_info: DebugInfoCollection = pydantic.Field(
        default_factory=DebugInfoCollection
    )

    @property
    def main_func(self) -> NativeFunctionDefinition:
        return self.function_dict[MAIN_FUNCTION_NAME]  # type:ignore[return-value]

    @property
    def body(self) -> StatementBlock:
        return self.main_func.body

    @pydantic.validator("preferences", always=True)
    def _seed_suffix_randomizer(cls, preferences: Preferences) -> Preferences:
        SUFFIX_RANDOMIZER.seed(preferences.random_seed)
        return preferences

    def _get_qualified_direction(
        self, port_name: str, direction: PortDeclarationDirection
    ) -> PortDeclarationDirection:
        if port_name in self.main_func.port_declarations:
            return PortDeclarationDirection.Inout
        return direction

    @property
    def function_dict(self) -> Mapping[str, NamedParamsQuantumFunctionDeclaration]:
        return nameables_to_dict(self.functions)

    @pydantic.validator("functions", always=True)
    def _add_empty_main(
        cls, functions: List[NativeFunctionDefinition]
    ) -> List[NativeFunctionDefinition]:
        function_dict = nameables_to_dict(functions)
        if MAIN_FUNCTION_NAME not in function_dict:
            functions.append(_create_empty_main_function())
        return functions

    def get_model(self) -> SerializedModel:
        return SerializedModel(
            self.json(exclude_defaults=True, exclude_unset=True, indent=2)
        )

    @pydantic.validator("functions")
    def _validate_entry_point(
        cls, functions: List[NativeFunctionDefinition]
    ) -> List[NativeFunctionDefinition]:
        function_dict = nameables_to_dict(functions)
        if MAIN_FUNCTION_NAME not in function_dict:
            raise ClassiqValueError("The model must contain a `main` function")
        if any(
            pd.direction != PortDeclarationDirection.Output
            for pd in function_dict[MAIN_FUNCTION_NAME].port_declarations
        ):
            raise ClassiqValueError("Function 'main' cannot declare quantum inputs")

        return functions

    @pydantic.validator("constants")
    def _validate_constants(cls, constants: List[Constant]) -> List[Constant]:
        constant_definition_counts = Counter(
            [constant.name for constant in constants]
        ).items()
        multiply_defined_constants = {
            constant for constant, count in constant_definition_counts if count > 1
        }
        if len(multiply_defined_constants) > 0:
            raise ClassiqValueError(
                f"The following constants were defined more than once: "
                f"{multiply_defined_constants}"
            )
        return constants

    def json_no_preferences_and_constraints(self) -> str:
        return self.json(
            indent=2,
            exclude={
                "constraints",
                "execution_preferences",
                "preferences",
            },
        )
