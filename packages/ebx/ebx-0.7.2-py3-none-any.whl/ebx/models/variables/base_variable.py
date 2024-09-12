from pydantic import BaseModel
from typing import Optional, Any

class BaseVariable(BaseModel):
    """A base abstract variable model."""
    key: str
    """The key of the variable."""
    type: str
    """The type of the variable."""
    name: Optional[str] = None
    """The name of the variable."""
    description: Optional[str] = None
    """The description of the variable."""
    value: Any
    """The value of the variable."""