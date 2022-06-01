from pydantic import BaseModel


class TaskID(BaseModel):
    id: str
