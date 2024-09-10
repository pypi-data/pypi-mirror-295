import csv
import re

from pydantic import BaseModel, Field, field_validator

from plurally.models.misc import Table
from plurally.models.node import Node
from plurally.models.utils import create_dynamic_model


class FormatText(Node):
    DESC = """
    Format text using a template.
    """.strip()

    class InitSchema(Node.InitSchema):
        template: str = Field(
            description="Template to format the text, example: Hello, {name}! I like {food}.",
            examples=["Hello, {name}, I like {food}."],
            format="textarea",
        )

        @field_validator("template")
        def check_template(cls, value):
            if not re.findall(r"{([^{}]+)}", value):
                raise ValueError("Template should contain at least one NAMED variable")
            return value

    class InputSchema(Node.InputSchema):
        text: str = Field(
            description="Text to format.",
            examples=["Hello, world!"],
            format="textarea",
        )

    class OutputSchema(BaseModel):
        formatted_text: str = Field(
            description="The text formatted using the template.",
        )

    def __init__(self, init_inputs: InitSchema):
        self.template = init_inputs.template
        super().__init__(init_inputs)

    def _set_schemas(self) -> None:
        # create pydantic model from output_fields
        self.InputSchema = create_dynamic_model(
            "InputSchema", self.vars, base=Node.InputSchema
        )

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value
        self.vars = re.findall(r"{(.*?)}", value)

    def forward(self, node_input):
        formatted_text = self.template.format(**node_input.model_dump())
        self.outputs["formatted_text"] = formatted_text

    def serialize(self):
        return {
            "template": self.template,
            "input_schema": self.InputSchema.model_json_schema(),
            **super().serialize(),
        }


class FormatTable(Node):
    DESC = """
    Format a table to text using a template.
    """.strip()

    class InitSchema(Node.InitSchema):
        prefix: str = Field(
            "",
            description="Prefix to add to the formatted text.",
            examples=["This is before the text."],
        )
        suffix: str = Field(
            "",
            description="Suffix to add to the formatted text.",
            examples=["This is after"],
        )
        separator: str = Field(
            ", ",
            description="Separator to use between rows.",
            examples=[", "],
        )
        template: str = Field(
            description="Template to format each row, example, every variable should be a table column.",
            examples=["Hello, {name}, I like {food}."],
            format="textarea",
        )

        @field_validator("template")
        def check_template(cls, value):
            if not re.findall(r"{([^{}]+)}", value):
                raise ValueError("Template should contain at least one NAMED variable")
            return value

    class InputSchema(Node.InputSchema):
        table: Table = Field(
            description="Table to format.",
        )

    class OutputSchema(BaseModel):
        formatted_text: str = Field(
            description="The table's content formatted to text.",
        )

    def __init__(self, init_inputs: InitSchema):
        self.template = init_inputs.template
        self.prefix = init_inputs.prefix
        self.suffix = init_inputs.suffix
        self.separator = init_inputs.separator

        super().__init__(init_inputs)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value
        self.vars = re.findall(r"{(.*?)}", value)

    def forward(self, node_input: InputSchema):
        row_str = []
        for row in node_input.table.data:
            formatted_text = self.template.format(**row)
            row_str.append(formatted_text)
        formatted_text = self.prefix + self.separator.join(row_str) + self.suffix
        self.outputs["formatted_text"] = formatted_text

    def serialize(self):
        return super().serialize() | {
            "template": self.template,
            "prefix": self.prefix,
            "suffix": self.suffix,
            "separator": self.separator,
        }


class CsvToTable(Node):
    DESC = """
    Convert CSV text to a table.
    """.strip()

    class InitSchema(Node.InitSchema):
        delimiter: str = Field(
            ",",
            description="Delimiter to use between columns.",
            examples=[","],
        )

    class InputSchema(Node.InputSchema):
        csv: str = Field(
            description="CSV string to convert to a table.",
            examples=["name,age\nAlice,25\nBob,30"],
            format="textarea",
        )

    class OutputSchema(BaseModel):
        data: Table = Field(
            description="The table converted from the CSV string.",
        )

    def __init__(self, init_inputs: InitSchema):
        self.delimiter = init_inputs.delimiter
        super().__init__(init_inputs)

    def forward(self, node_input: InputSchema):
        table = Table(
            data=csv.DictReader(
                node_input.csv.splitlines(),
                delimiter=self.delimiter,
            )
        )
        self.outputs["data"] = table

    def serialize(self):
        return super().serialize() | {
            "delimiter": self.delimiter,
        }


__all__ = [
    "FormatText",
    "FormatTable",
    "CsvToTable",
]
