import uuid
from typing import Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class Size(BaseModel):
    width: float
    length: float


class RobotPydantic(BaseModel):
    id: uuid.UUID
    name: str
    size: Size
    hash: str

    model_config = ConfigDict(from_attributes=True)



class Variable(BaseModel):
    var: str
    type: Literal[
        "latitude",
        "longitude",
        "orientation",
        "int",
        "float",
        "string",
        "enum",
        "enum_multiple",
    ]
    normal_name: Optional[str] = Field(None, alias="normalName")
    variants: Optional[list[str]] = None
    is_required: Optional[bool] = Field(None, alias="isRequired")
    default_variant_index: Optional[int] = Field(None, alias="defaultVariantIndex")


class FunctionPydantic(BaseModel):
    name: str
    description: str
    route: str
    input: list[Variable]
    type: str

    model_config = ConfigDict(from_attributes=True)
