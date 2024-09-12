from .base_variable import BaseVariable
from typing import Literal
from datetime import datetime

class DateVariable(BaseVariable):
    type: Literal['date']
    value: datetime