from pydantic import BaseModel


class TaskStatus(BaseModel):
    progress: str
