from pydantic import BaseModel
from .base_variable import BaseVariable
from typing import Literal
from datetime import datetime


class DataRangeValueVariable(BaseModel):
    start_date: datetime
    end_date: datetime

class DateRangeVariable(BaseVariable):
    type: Literal['date range']
    value: DataRangeValueVariable