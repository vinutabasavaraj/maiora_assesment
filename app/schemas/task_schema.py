from pydantic import BaseModel
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: str  
    due_date: datetime
    completed: bool
    extension : str

class Task(TaskBase):
    id: int
    owner_id: int
