import ebx
from ebx.models.run import Run
from ebx.models.project_spec import ProjectSpec

def test_list_runs():
    ebx.auth_using_creds()
    
    runs = ebx.list_runs()

    assert len(runs) > 0
    assert isinstance(runs[0], Run)


def test_list_run():
    ebx.auth_using_creds()
    
    runs = ebx.list_runs()
    run = ebx.get_run(runs[0].id)

    assert isinstance(run, Run)
    assert run.id == runs[0].id
    assert run.status == runs[0].status
    assert run.started_at == runs[0].started_at
    assert run.completed_at == runs[0].completed_at
    assert run.variables == runs[0].variables
    assert run.exec_parameters == runs[0].exec_parameters


def test_get_run_get_charts():
    ebx.auth_using_creds()
    
    runs = ebx.list_runs()
    run = ebx.get_run(runs[0].id)
    charts = ebx.get_charts(run.id)

    assert isinstance(charts, list)

def test_get_run_get_layers():
    ebx.auth_using_creds()
    
    runs = ebx.list_runs()
    run = ebx.get_run(runs[0].id)
    layers = ebx.get_layers(run.id)

    assert isinstance(layers, list)

def test_get_run_get_tables():
    ebx.auth_using_creds()
    
    runs = ebx.list_runs()
    run = ebx.get_run(runs[0].id)
    tables = ebx.get_tables(run.id)

    assert isinstance(tables, list)

def test_get_run_get_status():
    ebx.auth_using_creds()
    
    runs = ebx.list_runs()
    run = ebx.get_run(runs[0].id)
    status = ebx.get_run_status(run.id)

    assert status == run.status


def test_can_create_run():
    ebx.auth_using_creds()
    
    projects = ebx.list_projects()
    project = projects[0]

    spec = ProjectSpec(project_id=project.id)

    run_id = ebx.create_run(spec)
    run = ebx.get_run(run_id)

    assert isinstance(run_id, str)
    assert run.id == run_id