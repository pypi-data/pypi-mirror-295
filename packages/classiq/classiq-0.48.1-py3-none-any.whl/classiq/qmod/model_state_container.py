from typing import Dict

from classiq.interface.generator.constant import Constant
from classiq.interface.generator.types.enum_declaration import EnumDeclaration
from classiq.interface.generator.types.qstruct_declaration import QStructDeclaration
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.model.native_function_definition import NativeFunctionDefinition


class ModelStateContainer:
    enum_decls: Dict[str, EnumDeclaration]
    type_decls: Dict[str, StructDeclaration]
    qstruct_decls: Dict[str, QStructDeclaration]
    native_defs: Dict[str, NativeFunctionDefinition]
    constants: Dict[str, Constant]


QMODULE = ModelStateContainer()
