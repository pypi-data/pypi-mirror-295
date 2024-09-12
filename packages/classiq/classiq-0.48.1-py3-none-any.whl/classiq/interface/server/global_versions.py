from datetime import date
from typing import Any, Dict

import pydantic
from pydantic import BaseModel


class DeprecationInfo(BaseModel):
    deprecation_date: date = pydantic.Field()
    removal_date: date = pydantic.Field()


class GlobalVersions(BaseModel):
    deprecated: Dict[str, DeprecationInfo] = pydantic.Field()
    deployed: Dict[str, Any] = pydantic.Field()
