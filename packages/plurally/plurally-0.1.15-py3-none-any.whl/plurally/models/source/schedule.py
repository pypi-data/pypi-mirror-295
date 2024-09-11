from datetime import datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field

from plurally.models.node import Node


class ScheduleUnit(str, Enum):
    MINUTE = "minutes"
    HOUR = "hours"
    DAY = "days"
    WEEK = "weeks"


class Schedule(Node):

    class InitSchema(Node.InitSchema):
        every: int = Field(
            description="The number of units to wait before executing the next block"
        )
        unit: ScheduleUnit = Field(
            description="The unit of time to wait before executing the next block"
        )
        first: datetime = Field(
            None,
            description="The first time to execute the block. If not provided, the current time will be used.",
        )

    class InputSchema(Node.InputSchema):
        pass

    class OutputSchema(BaseModel):
        run: bool = Field(
            False,
            description="Whether the next block should be executed or not",
        )

    def __init__(self, init_inputs: InitSchema):
        self.every = init_inputs.every
        self.unit = init_inputs.unit
        self.last_exec = init_inputs.first if init_inputs.first else datetime.now()
        super().__init__(init_inputs)

    @property
    def next(self):
        return self.last_exec + timedelta(**{self.unit.value: self.every})

    def forward(self, **kwargs):
        now = datetime.now()
        if now >= self.next:
            self.last_exec = now
            self.outputs = {"run": True}
        else:
            self.outputs = {"run": False}

    def serialize(self):
        serialized = super().serialize()
        serialized["every"] = self.every
        serialized["unit"] = self.unit
        serialized["first"] = self.next
        return serialized
