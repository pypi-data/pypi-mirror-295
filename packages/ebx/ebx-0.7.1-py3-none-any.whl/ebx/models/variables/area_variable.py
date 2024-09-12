from .base_variable import BaseVariable
from typing import Union, Literal
from ebx.typings.areas import Areas

class AreaVariable(BaseVariable):
    type: Literal['area']
    value: Union[Areas, str]