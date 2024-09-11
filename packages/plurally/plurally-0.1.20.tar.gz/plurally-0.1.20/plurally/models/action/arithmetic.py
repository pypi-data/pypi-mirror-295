import operator

from pydantic import BaseModel

from plurally.models.node import Node


class PrintNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.inputs["value"] = None

    def forward(self):
        ...
        # """Print the input value."""
        # name, handler = self.inputs["value"]
        # value = flow[name].outputs[handler]
        # if value is not None:
        #     print(f"{self.name}: {value}")


class BinaryOpNode(Node):
    _OP = None

    class InputSchema(Node.InputSchema):
        left: float | int
        right: float | int

    class OutputSchema(BaseModel):
        result: float

    def forward(self, node_input: InputSchema):
        self.outputs["result"] = self._OP(node_input.left, node_input.right)


class Multiply(BinaryOpNode):
    _OP = operator.mul


class Add(BinaryOpNode):
    _OP = operator.add


class Subtract(BinaryOpNode):
    _OP = operator.sub


class Divide(BinaryOpNode):
    _OP = operator.truediv


class Mod(BinaryOpNode):
    _OP = operator.mod


__all__ = [
    "Add",
    "Multiply",
    "Mod",
    "Divide",
    "Subtract",
]
