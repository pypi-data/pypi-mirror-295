from typing import Any, Dict, Optional, Tuple

import pydantic

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.arith import number_utils
from classiq.interface.helpers.custom_pydantic_types import PydanticFloatTuple
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)


class RegisterArithmeticInfo(HashablePydanticBaseModel):
    size: pydantic.PositiveInt
    is_signed: bool = pydantic.Field(default=False)
    fraction_places: pydantic.NonNegativeInt = pydantic.Field(default=0)
    bypass_bounds_validation: bool = pydantic.Field(default=False)
    bounds: PydanticFloatTuple = pydantic.Field(default=None)

    @pydantic.root_validator(pre=True)
    def _remove_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "name" in values:
            values.pop("name")
        return values

    @staticmethod
    def get_maximal_bounds(
        *, size: int, is_signed: bool, fraction_places: int
    ) -> Tuple[float, float]:
        lb = 0 if not is_signed else -(2 ** (size - 1))
        ub = 2**size - 1 if not is_signed else 2 ** (size - 1) - 1
        fraction_factor = float(2**-fraction_places)
        return (lb * fraction_factor, ub * fraction_factor)

    @pydantic.validator("bounds", always=True)
    def _validate_bounds(
        cls, bounds: Optional[PydanticFloatTuple], values: Dict[str, Any]
    ) -> PydanticFloatTuple:
        size = values.get("size")
        is_signed = values.get("is_signed", False)
        fraction_places = values.get("fraction_places", 0)
        if not isinstance(size, int):
            raise ClassiqValueError("RegisterArithmeticInfo must have an integer size")

        maximal_bounds = cls.get_maximal_bounds(
            size=size, is_signed=is_signed, fraction_places=fraction_places
        )
        if bounds is None:
            return maximal_bounds

        trimmed_bounds = (
            number_utils.limit_fraction_places(min(bounds), fraction_places),
            number_utils.limit_fraction_places(max(bounds), fraction_places),
        )
        if not values.get("bypass_bounds_validation", False):
            assert min(trimmed_bounds) >= min(maximal_bounds), "Illegal bound min"
            assert max(trimmed_bounds) <= max(maximal_bounds), "Illegal bound max"
        return trimmed_bounds

    def limit_fraction_places(self, machine_precision: int) -> "RegisterArithmeticInfo":
        truncated_bits: int = max(self.fraction_places - machine_precision, 0)
        return RegisterArithmeticInfo(
            size=self.size - truncated_bits,
            is_signed=self.is_signed,
            fraction_places=self.fraction_places - truncated_bits,
            bounds=self.bounds,
            bypass_bounds_validation=self.bypass_bounds_validation,
        )

    @property
    def is_boolean_register(self) -> bool:
        return (not self.is_signed) and (self.size == 1) and (self.fraction_places == 0)

    @property
    def is_frac(self) -> bool:
        return self.fraction_places > 0

    @property
    def integer_part_size(self) -> pydantic.NonNegativeInt:
        return self.size - self.fraction_places

    class Config:
        frozen = True


class RegisterUserInput(RegisterArithmeticInfo):
    name: str = pydantic.Field(default="")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._fields_to_skip_in_hash = frozenset({"name"})

    @pydantic.root_validator(pre=True)
    def _remove_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values

    def revalued(self, **kwargs: Any) -> "RegisterUserInput":
        return self.copy(update=kwargs)

    @classmethod
    def from_arithmetic_info(
        cls, info: RegisterArithmeticInfo, name: str = ""
    ) -> "RegisterUserInput":
        return RegisterUserInput(
            name=name,
            size=info.size,
            is_signed=info.is_signed,
            fraction_places=info.fraction_places,
            bounds=info.bounds,
        )
