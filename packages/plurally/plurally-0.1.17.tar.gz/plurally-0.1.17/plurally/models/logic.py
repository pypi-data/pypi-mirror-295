from typing import Dict, List

from pydantic import BaseModel, Field

from plurally.models.node import Node
from plurally.models.utils import create_dynamic_model


class Switch(Node):

    class InitSchema(Node.InitSchema):
        possible_values: List[str] = Field(
            title="Possible Values",
            description="The possible values that the input can take.",
            example=["A", "B", "C"],
        )

    class InputSchema(Node.InputSchema):
        value: str = Field(
            title="Value",
            description="The value to switch on.",
        )

    class OutputSchema(BaseModel):
        key_vals: Dict[str, str]

    def __init__(self, init_inputs: InitSchema) -> None:
        self._possible_values = init_inputs.possible_values
        super().__init__(init_inputs)

    @property
    def possible_values(self):
        return self._possible_values

    @possible_values.setter
    def possible_values(self, value):
        self._possible_values = value
        self._set_schemas()

    def _set_schemas(self) -> None:
        # create pydantic model from fields
        self.OutputSchema = create_dynamic_model(
            "OutputSchema",
            self.possible_values,
            defaults={val: None for val in self.possible_values},
            types={val: bool for val in self.possible_values},
        )

    def forward(self, node_input: InputSchema):
        assert (
            node_input.value in self.possible_values
        ), f"Value {node_input.value} not in possible values."
        for val in self.possible_values:
            self.outputs[val] = False
        self.outputs[node_input.value] = True

    def serialize(self):
        return {
            **super().serialize(),
            "possible_values": self.possible_values,
            "output_schema": self.OutputSchema.model_json_schema(),
        }


__all__ = ["Switch"]
