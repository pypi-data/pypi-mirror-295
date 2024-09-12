import ebx
from ebx.config import ClientConfig
from ebx.persistence.in_memory import InMemoryPersistence
from pytest_httpx import HTTPXMock
from .constants import PROJECT_DATA, RUN, CHART_OUTPUT, TABLE_OUTPUT, RUN_LAYER
import pytest
from ebx.models.run import Run

def test_global_context():
    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    assert isinstance(ebx.get_client(), ebx.client.Client)


def test_list_projects(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={
        "data": [PROJECT_DATA]
    })

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    projects = ebx.list_projects()

    assert len(projects) == 1
    assert projects[0].id == PROJECT_DATA['id']

def test_get_project(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'data':PROJECT_DATA})

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    project = ebx.get_project(PROJECT_DATA['id'])

    assert project.id == PROJECT_DATA['id']
    

def test_get_runs(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'data': [RUN]})

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    runs = ebx.list_runs(limit=10)

    assert len(runs) == 1
    assert runs[0].id == RUN['id']

def test_get_run(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'data':RUN})

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    run = ebx.get_run(RUN['id'])

    assert run.id == RUN['id']

def test_create_run(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'data':{"run_id":"12345"}})

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    id = ebx.create_run(ebx.ProjectSpec(type="template",project_id="12345"))

    assert id == '12345'

def test_get_run_status(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'data':RUN})

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    status = ebx.get_run_status(RUN['id'])

    assert status == RUN['status']

def test_get_run_charts(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'data':[CHART_OUTPUT]})

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    charts = ebx.get_charts(RUN['id'])

    assert len(charts) == 1

def test_get_run_tables(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'data':[TABLE_OUTPUT]})

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    tables = ebx.get_tables(RUN['id'])

    assert len(tables) == 1

def test_get_run_layers(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'data':[RUN_LAYER]})

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    layers = ebx.get_layers(RUN['id'])

    assert len(layers) == 1

@pytest.mark.asyncio
async def test_follow_run(httpx_mock: HTTPXMock):
    httpx_mock.add_response( json={'data':{'status':'inProgress'}})
    httpx_mock.add_response( json={'data':{'status':'completed'}})
    httpx_mock.add_response( json={'data':RUN})


    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)

    run = await ebx.follow_run(RUN['id'], timeout=5, wait_seconds=1)

    assert isinstance(run, Run)
    assert run.id == RUN['id']

@pytest.mark.asyncio
async def test_follow_run_raises_error_on_timeout(httpx_mock: HTTPXMock):
    httpx_mock.add_response( json={'data':{'status':'inProgress'}})
    httpx_mock.add_response( json={'data':{'status':'inProgress'}})

    memory_persistence = InMemoryPersistence()
    config = ClientConfig(persistence_driver=memory_persistence)

    ebx.auth_using_env(config=config)
    with pytest.raises(Exception):
        await ebx.follow_run(RUN['id'], timeout=5, wait_seconds=3)
