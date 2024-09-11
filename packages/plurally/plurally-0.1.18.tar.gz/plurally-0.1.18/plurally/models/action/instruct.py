from enum import Enum
from typing import Any, Dict, List

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

from plurally.models.misc import Table
from plurally.models.node import Node
from plurally.models.utils import BaseEnvVars, create_dynamic_model


class InstructModel(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"


class Instruct(Node):
    class InitSchema(Node.InitSchema):
        model: InstructModel = Field(
            InstructModel.GPT_4O_MINI,
            title="Model",
            description="The OpenAI model to use.",
            examples=["gpt-3.5-turbo"],
        )
        instruct: str = Field(
            title="Instructions",
            description="Instructions for the AI model.",
            format="textarea",
            examples=["Write a support email."],
        )
        is_table: bool = Field(
            False,
            title="Table Output",
            description="Whether the output is a table. For instance, if you want ChatGPT to output a list of outputs with the same columns, you should tick this.",
            examples=[True, False],
        )
        output_fields: List[str] = Field(
            ["output"],
            title="Outputs",
            description="The different output attributes of the AI model",
            examples=["output1", "output2"],
        )

    class OutputSchema(BaseModel):
        key_vals: Dict[str, str]

    class InputSchema(Node.InputSchema):
        contexts: List[str] = None

    class EnvVars(BaseEnvVars):
        OPENAI_API_KEY: str = Field(
            None, title="OpenAI API Key", examples=["sk-1234567890abcdef"]
        )

    def __init__(
        self,
        init_inputs: InitSchema,
    ) -> None:
        self.is_table = init_inputs.is_table
        self._client = None  # lazy init
        self.model = init_inputs.model
        self.instruct = init_inputs.instruct
        self._output_fields = init_inputs.output_fields
        super().__init__(init_inputs)

    def _set_schemas(self) -> None:
        # create pydantic model from output_fields
        self.instruct_schema = create_dynamic_model("OutputSchema", self.output_fields)
        if self.is_table:
            self.instruct_schema = List[self.instruct_schema]

            class OutputSchema(BaseModel):
                data: Table = Field(
                    description=f"The ouputs converted to a table, columns are the output fields: {self.output_fields}.",
                )

            self.OutputSchema = OutputSchema
        else:
            self.OutputSchema = self.instruct_schema

    @property
    def output_fields(self):
        return self._output_fields

    @output_fields.setter
    def output_fields(self, value):
        self._output_fields = value
        self._set_schemas()

    @property
    def client(self):
        if self._client is None:
            self._client = instructor.from_openai(OpenAI())
        return self._client

    def build_messages(self, contexts: List[str] = None) -> str:
        prompt = self.instruct + "\n"
        for ix_ctx, ctx in enumerate((contexts or [])):
            prompt += f'\nContext {ix_ctx + 1}: """\n{ctx}\n"""'
        return [
            {"role": "assistant", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

    def create(self, messages: List[Dict[str, str]]) -> Any:
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_model=self.instruct_schema,
        )

    def forward(self, node_input: InputSchema) -> Any:
        messages = self.build_messages(node_input.contexts)
        output: self.OutputSchema = self.create(messages)

        if self.is_table:
            self.outputs["data"] = Table(data=[o.model_dump() for o in output])
        else:
            self.outputs = output.model_dump()

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            "instruct": self.instruct,
            "outputs": self.outputs,
            "output_fields": self.output_fields,
            "output_schema": self.OutputSchema.model_json_schema(),
            "is_table": self.is_table,
            "model": self.model,
        }
