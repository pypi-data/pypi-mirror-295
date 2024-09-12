"""Defines the project specification used to create runs from projects."""

"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, model_validator
from .exec_parameters import Config
from .variables import VariableConfig

class ProjectSpecType(str, Enum):
    """The type of project spec."""
    TEMPLATE = 'template'
    href_TEMPLATE = 'href_template'
    # INLINE = 'inline' # not yet supported

class ProjectSpec(BaseModel):
    """The project spec."""
    type: Optional[str] = ProjectSpecType.TEMPLATE.value
    project_id: Optional[str] = None
    href: Optional[str] = None # TODO: currently using string here, but we could use either Path or Query class from fastapi
    include_geometry: Optional[bool] = False
    generate_thumbnails: Optional[bool] = False
    variables: List[VariableConfig] = []
    exec_parameters: Optional[Config] = None

    @model_validator(mode='after')
    def href_must_be_provided_if_type_is_href_template(self):
        """Validates that the href is provided if the type is href_template."""
        if self.type == ProjectSpecType.href_TEMPLATE and self.href is None:
            raise ValueError('href must be provided if type is href_template')
        
        return self

    @model_validator(mode='after')
    def href_must_not_be_provided_if_type_is_template(self):
        """Validates that the href is not provided if the type is template."""
        if self.type != ProjectSpecType.href_TEMPLATE and self.href is not None:
            raise ValueError('href must not be provided if type is not href_template')
        
        return self
    
    @model_validator(mode='after')
    def project_id_must_be_provided_if_type_is_template(self):
        """Validates that the project_id is provided if the type is template."""
        if self.type == ProjectSpecType.TEMPLATE and self.project_id is None:
            raise ValueError('project_id must be provided if type is template')
        
        return self
    
    @model_validator(mode='after')
    def project_id_must_not_be_provided_if_type_is_href_template(self):
        """Validates that the project_id is not provided if the type is href_template."""
        if self.type != ProjectSpecType.TEMPLATE and self.project_id is not None:
            raise ValueError('project_id must not be provided if type is not template')
        
        return self

    def get_project_id(self):
        """Returns the project id from the project spec."""
        if self.type == ProjectSpecType.TEMPLATE:
            return self.project_id
        
        if self.type == ProjectSpecType.href_TEMPLATE:
            return self.href.split('/')[-1]
        
        raise ValueError(f'project_id cannot be retrieved for project spec type {self.type}')