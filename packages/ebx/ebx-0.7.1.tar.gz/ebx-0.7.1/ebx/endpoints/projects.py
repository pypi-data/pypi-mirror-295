"""Defines the projects endpoints."""

"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
from ebx.client import get_client, register_endpoint
from ebx.models.project import Project
from typing import List

@register_endpoint()
def list_projects(title: str = None) -> List[Project]:
    """Lists the projects.

    Returns:
        Projects List: The list of projects.
    """
    client = get_client()
    query_params = {}
    if title is not None:
        query_params["title"] = title
    
    res = client.get("/projects/", query_params=query_params)
    
    return [Project(**project) for project in res.get("data")]

@register_endpoint()
def get_project(project_id: str) -> Project:
    """Gets a specified project by id.
    
    Args:
        project_id (str): The id of the project.

    Returns:
        project: The project.
    """
    client = get_client()

    res = client.get(f"/projects/{project_id}")
    
    return Project(**res.get('data'))