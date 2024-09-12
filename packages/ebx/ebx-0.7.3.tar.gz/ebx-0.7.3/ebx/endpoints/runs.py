"""Defines the runs endpoints."""

"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
from ebx.client import get_client, register_endpoint
from ebx.models.project_spec import ProjectSpecType, ProjectSpec
from ebx.models.run import Run
from ebx.models.output import Output
from ebx.models.layer import Layer
from typing import List
import asyncio
import time
import json
from ebx.encoder import PlotlyJSONEncoder

@register_endpoint()
def list_runs(limit: int = 10) -> List[Run]:
    """Lists the runs.

    Args:
        limit (int, optional): The number of runs to return. Defaults to 10.

    Returns:
        Run List: The list of runs.
    """
    client = get_client()

    params = {
        "limit": limit
    }

    res = client.get("/runs/", query_params=params)

    return [Run(**run) for run in res.get("data")]

@register_endpoint()
def get_run(run_id: str) -> Run:
    """Gets a specified run by id.
    
    Args:
        run_id (str): The id of the run.

    Returns:
        Run: The run.
    """
    client = get_client()

    res = client.get(f"/runs/{run_id}")
    
    return Run(**res.get("data"))

@register_endpoint()
def get_charts(run_id: str, filter: str = None) -> list:
    """returns only the charts from a specified run

    Args:
        run_id (str): The id of the run.
        filter (str): optional filter which will be applied to the title of the charts

    Returns:
        list: a list of the charts from this run
    """
    client = get_client()
    query_params = None
    uri = f"/runs/{run_id}/charts"
    if filter:
        query_params = {'title': filter}
        print(f"Filtering charts with filter '{query_params}'")
    res = client.get(uri, query_params)
    return list(map(lambda layer: Output(**layer), res.get("data")))

@register_endpoint()
def get_tables(run_id: str, filter: str = None) -> list:
    """returns only the tables from a specified run

    Args:
        run_id (str): The id of the run.
        filter (str): optional filter which will be applied to the title of the tables

    Returns:
        list: a list of the tables from this run
    """
    client = get_client()
    query_params = None
    if filter:
        query_params = {'title': filter}
        print(f"Filtering tables with filter '{query_params}'")
    uri = f"/runs/{run_id}/tables"
    res = client.get(uri, query_params)
    return list(map(lambda layer: Output(**layer), res.get("data")))

@register_endpoint()
def get_layers(run_id: str, filter: str = None) -> list:
    """returns only the layers from a specified run

    Args:
        run_id (str): The id of the run.
        filter (str): optional filter which will be applied to the name of the layers
    Returns:
        list: a list of the layers from this run
    """
    client = get_client()
    query_params = None
    if filter:
        query_params = {'title': filter}
        print(f"Filtering layers with filter '{query_params}'")
    res = client.get(f"/runs/{run_id}/layers", query_params)
    return list(map(lambda layer: Layer(**layer), res.get("data")))

@register_endpoint()
def get_run_status(run_id: str) -> str:
    """Gets the current status of a run.
    
    Args:
        run_id (str): The id of the run.

    Returns:
        The run status.
    """

    client = get_client()

    res = client.get(f"/runs/{run_id}/status")
    
    return res.get("data").get('status')

# create run makes post request to /runs
# returns run id
# TODO: update to work with href method
@register_endpoint()
def create_run(project_spec: ProjectSpec) -> str:
    """Creates a run using the specified project.
    
    Args:
        project_spec (ProjectSpec): the project spec to use for the run

    Returns:
        str: The id of the run.
    """

    client = get_client()

    if not isinstance(project_spec.include_geometry, bool):
        raise TypeError("include_geometry must be a boolean.")
    
    if not isinstance(project_spec.generate_thumbnails, bool):
        raise TypeError("generate_thumbnails must be a boolean.")

    body = project_spec.model_dump()
    
    json_body = json.dumps(body,cls=PlotlyJSONEncoder)
    body = json.loads(json_body)

    res = client.post("/runs/", body)
    
    return res.get("data").get('run_id')

@register_endpoint()
async def follow_run(run_id: str, wait_seconds: int = 10, timeout: int = 60 * 5) -> Run:
    """Follows a run until it is complete, or after 5 minutes.
    
    Args:
        run_id (str): The id of the run.
        
    Returns:
        Run: The run.

    Raises:
        Exception: If the run is not complete after 5 minutes.
    """
    # create a poller to continuously poll the run using get_run with status only
    status = None
    start_time = time.time()
    while status in ['running', 'started', 'inProgress'] or status is None:
        status = get_run_status(run_id)
        await asyncio.sleep(wait_seconds)
        if time.time() - start_time > timeout:
            raise Exception(f"Run {run_id} did not complete after {timeout} seconds.")

    return get_run(run_id)