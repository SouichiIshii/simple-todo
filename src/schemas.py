import datetime
from enum import Enum

from pydantic import BaseModel

class Status(str, Enum):
    not_yet = "未着手"
    in_progress = "進行中"
    done = "完了"

class NewTaskInfo(BaseModel):
    task_name: str
    registration_date: datetime.date
    deadline_date: datetime.date
    status: Status

class UpdatedTaskInfo(BaseModel):
    task_name: str
    deadline_date: datetime.date
    status: Status