from pydantic import BaseModel, Field, field_validator

from plurally.models.node import Node


class ConstantSource(Node):
    class InputSchema(Node.InputSchema): ...

    def __init__(self, init_inputs) -> None:
        super().__init__(init_inputs)
        self.outputs["value"] = init_inputs.value

    def __call__(self):
        """No evaluation needed, constant value is already set."""
        ...

    def serialize(self):
        payload = super().serialize()
        payload["value"] = self.outputs["value"]
        return payload


class Text(ConstantSource):

    class InitSchema(ConstantSource.InitSchema):
        value: str = Field(
            title="Text",
            description="The constant text value.",
            examples=["hello"],
            format="textarea",
        )

    class OutputSchema(BaseModel):
        value: str = Field(json_schema_extra={"constant": True})

        @field_validator("value")
        def strip_value(cls, value):
            return value.strip()


class Integer(ConstantSource):

    class InitSchema(ConstantSource.InitSchema):
        value: int

    class OutputSchema(BaseModel):
        value: int = Field(json_schema_extra={"constant": True})


class Number(ConstantSource):

    class InitSchema(ConstantSource.InitSchema):
        value: float

    class OutputSchema(BaseModel):
        value: float = Field(json_schema_extra={"constant": True})


class Boolean(ConstantSource):

    class InitSchema(ConstantSource.InitSchema):
        value: bool

    class OutputSchema(BaseModel):
        value: bool = Field(json_schema_extra={"constant": True})


__all__ = ["Text", "Integer", "Number", "Boolean"]
