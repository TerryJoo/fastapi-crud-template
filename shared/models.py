from datetime import datetime

from pydantic import BaseModel


class CreatedAtModel(BaseModel):
    created_at: datetime


class TimestampModel(CreatedAtModel):
    created_at: datetime
    updated_at: datetime

