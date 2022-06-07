from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator


class BotInfo(BaseModel):
    username: str
    fullname: str
    users_live: int
    users_die: int
    users_empty: int
    groups_live: int
    groups_die: int
    users_in_groups: int
    arabic: Optional[str]
    male: Optional[str]
    female: Optional[str]
    date: Optional[datetime]

    @validator('date', pre=True)
    def convert_date(date: str):
        return datetime.fromisoformat(date.replace(',' , ''))