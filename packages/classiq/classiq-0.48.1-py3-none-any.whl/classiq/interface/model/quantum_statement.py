from dataclasses import dataclass
from typing import Any, Callable, Dict, Mapping, Optional, Sequence

import pydantic
from pydantic import Extra, root_validator

from classiq.interface.ast_node import ASTNode
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator
from classiq.interface.model.handle_binding import (
    ConcreteHandleBinding,
    HandleBinding,
)


class QuantumStatement(ASTNode):
    kind: str

    class Config:
        extra = Extra.forbid

    @root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", cls.__name__)  # type: ignore[attr-defined]


@dataclass
class HandleMetadata:
    handle: HandleBinding
    readable_location: Optional[str] = None


class QuantumOperation(QuantumStatement):
    _generative_blocks: Dict[str, Callable] = pydantic.PrivateAttr(default_factory=dict)

    @property
    def wiring_inputs(self) -> Mapping[str, HandleBinding]:
        return dict()

    @property
    def inputs(self) -> Sequence[HandleBinding]:
        return list(self.wiring_inputs.values())

    @property
    def wiring_inouts(self) -> Mapping[str, ConcreteHandleBinding]:
        return dict()

    @property
    def inouts(self) -> Sequence[HandleBinding]:
        return list(self.wiring_inouts.values())

    @property
    def wiring_outputs(self) -> Mapping[str, HandleBinding]:
        return dict()

    @property
    def outputs(self) -> Sequence[HandleBinding]:
        return list(self.wiring_outputs.values())

    @property
    def readable_inputs(self) -> Sequence[HandleMetadata]:
        return [HandleMetadata(handle=handle) for handle in self.inputs]

    @property
    def readable_inouts(self) -> Sequence[HandleMetadata]:
        return [HandleMetadata(handle=handle) for handle in self.inouts]

    @property
    def readable_outputs(self) -> Sequence[HandleMetadata]:
        return [HandleMetadata(handle=handle) for handle in self.outputs]

    def set_generative_block(self, block_name: str, py_callable: Callable) -> None:
        self._generative_blocks[block_name] = py_callable

    def get_generative_block(self, block_name: str) -> Callable:
        return self._generative_blocks[block_name]

    def has_generative_block(self, block_name: str) -> bool:
        return block_name in self._generative_blocks

    def is_generative(self) -> bool:
        return len(self._generative_blocks) > 0
