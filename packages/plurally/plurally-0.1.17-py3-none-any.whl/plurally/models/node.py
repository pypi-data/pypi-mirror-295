import abc
import uuid
from typing import List, Union, get_args

from loguru import logger
from pydantic import BaseModel, EmailStr, Field
from pydantic_core import ValidationError

from plurally.models.utils import BaseEnvVars

TYPE_ADAPTER = {
    EmailStr: str,
}


def is_type_compatible(input_field, output_field):
    # If output_type is a Union, extract all possible types
    input_type = TYPE_ADAPTER.get(input_field.annotation, input_field.annotation)
    output_type = TYPE_ADAPTER.get(output_field.annotation, output_field.annotation)
    # check if output_type is a List
    if hasattr(output_type, "__origin__") and output_type.__origin__ is Union:
        return any(
            issubclass(input_type, allowed_type)
            for allowed_type in get_args(output_type)
        )

    try:
        # Otherwise, simply check if input_type is a subclass of output_type
        if hasattr(output_type, "__origin__") and output_type.__origin__ is list:
            return issubclass(input_type, output_type.__args__[0])
        else:
            return issubclass(input_type, output_type)
    except Exception as e:
        raise ValueError(
            f"Error checking type compatibility: {input_type=}, {output_type=}"
        ) from e


class Node(abc.ABC):
    class InputSchema(BaseModel):
        run: bool = Field(
            True,
            title="Run",
            description="Whether to run the block.",
            examples=[True, False],
        )

    OutputSchema = None
    EnvVars: BaseEnvVars = None
    SensitiveFields = tuple()
    DESC = ""
    SCOPES: List[str] = None

    class InitSchema(BaseModel):
        name: str = Field(
            title="Block Name", description="Name of the block.", examples=["Block 1"]
        )
        pos_x: float = 0
        pos_y: float = 0

    def __init__(self, init_inputs: InitSchema, outputs=None):
        self._node_id = f"nd-{str(uuid.uuid4())}"
        self.name = init_inputs.name
        self.outputs = outputs or {}
        self._set_schemas()
        self._check_schemas()

        self.pos_x = init_inputs.pos_x
        self.pos_y = init_inputs.pos_y

    def _check_schemas(self):
        if self.InputSchema is None or not issubclass(self.InputSchema, BaseModel):
            raise ValueError(f"{type(self).__name__} must have an InputSchema")
        if self.OutputSchema is None or not issubclass(self.OutputSchema, BaseModel):
            raise ValueError(f"{type(self).__name__} must have an OutputSchema")

    def _set_schemas(self): ...

    @property
    def node_id(self):
        return self._node_id

    def validate_connection(
        self, src_node: "Node", output_node_id: str, input_node_id: str
    ):
        output_node_schema = src_node.OutputSchema.model_fields.get(output_node_id)
        input_node_schema = self.InputSchema.model_fields.get(input_node_id)

        if output_node_schema is None or input_node_schema is None:
            return True
        return is_type_compatible(output_node_schema, input_node_schema)

    def validate_inputs(self, **kwargs):
        try:
            return self.InputSchema(**kwargs)
        except ValidationError as e:
            raise ValueError(f"Invalid inputs for {self}, got={kwargs}") from e

    def __call__(self, **kwargs):
        """Override this method in child classes to define logic."""
        node_input = self.validate_inputs(**kwargs)
        logger.debug(f"Running {self} with inputs: {node_input}")
        self.forward(node_input)

    def forward(self, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and other.node_id == self.node_id

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, node_id={self.node_id[:7]})"

    def __hash__(self) -> int:
        return hash(self.node_id)

    def serialize(self):
        # outputs_to_serialize = None
        # if self.outputs is not None:
        #     outputs_to_serialize = {**self.outputs}
        #     for k, v in outputs_to_serialize.items():
        #         if isinstance(v, datetime):
        #             outputs_to_serialize[k] = v.isoformat()

        return {
            "kls": type(self).__name__,
            "name": self.name,
            "_node_id": self._node_id,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            # "outputs": outputs_to_serialize,
        }

    @classmethod
    def _parse(cls, **kwargs):
        return cls(cls.InitSchema(**kwargs))

    @classmethod
    def parse(cls, **kwargs):
        _node_id = kwargs.pop("_node_id")
        # outputs = kwargs.pop("outputs")
        obj = cls._parse(**kwargs)
        obj._node_id = _node_id
        obj.pos_x = kwargs.get("pos_x", 0)
        obj.pos_y = kwargs.get("pos_y", 0)

        # if outputs is not None:
        #     for k, v in outputs.items():
        #         if isinstance(v, datetime):
        #             outputs[k] = v.fromisoformat(v)

        # obj.outputs = outputs
        return obj
