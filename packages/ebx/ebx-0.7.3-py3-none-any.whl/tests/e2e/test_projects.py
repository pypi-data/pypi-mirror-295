import ebx
from ebx.models.project import Project

def test_list_projects():
    ebx.auth_using_creds()

    projects = ebx.list_projects()

    assert len(projects) > 0
    assert isinstance(projects[0], Project)


def test_list_project():
    ebx.auth_using_creds()

    projects = ebx.list_projects()
    project = ebx.get_project(projects[0].id)

    assert isinstance(project, Project)
    assert project.id == projects[0].id
    assert project.title == projects[0].title
    assert project.description == projects[0].description
    assert project.version == projects[0].version
    assert project.variables == projects[0].variables
    assert project.exec_parameters == projects[0].exec_parameters
    