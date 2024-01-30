from pydantic import BaseModel

class MessageBase(BaseModel):
    content: str

class Message(MessageBase):
    id: int
    task_id: int
    author_id: int
