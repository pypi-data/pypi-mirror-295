"""Class defining a project."""

"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
from dataclasses import dataclass
from .variables import VariableConfig
from .exec_parameters import Config
from typing import List, Optional
from pydantic import BaseModel
class Project(BaseModel):
    """Describes a project."""

    id: str
    """The id of the project."""

    title: str
    """The title of the project."""

    description:  Optional[str] = None
    """The description of the project."""

    version:  Optional[str] = None
    """The valid API version for the project."""

    variables: Optional[List[VariableConfig]] = []
    """The variables associated with the project."""

    exec_parameters: Optional[Config] = None
    """The execution parameters associated with the project."""