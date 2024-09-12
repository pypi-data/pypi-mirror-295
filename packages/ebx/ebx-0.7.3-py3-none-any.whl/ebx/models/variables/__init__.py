from .area_variable import AreaVariable
from .date_variable import DateVariable
from .date_range_variable import DateRangeVariable
from typing import Union, Annotated
from pydantic import Field

VariableConfig = Annotated[
    Union[AreaVariable, DateVariable, DateRangeVariable],
    Field(discriminator='type')
]