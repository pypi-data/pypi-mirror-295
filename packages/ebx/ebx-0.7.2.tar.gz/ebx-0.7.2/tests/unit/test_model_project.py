from ebx.models.project import Project
from ebx.typings.areas import PolygonFeatureCollection
from ebx.models.variables.date_range_variable import DataRangeValueVariable
from .constants import PROJECT_DATA

def test_project():
    project = Project(**PROJECT_DATA)
    assert project.id == PROJECT_DATA['id']
    assert project.title == PROJECT_DATA['title']
    assert project.version == PROJECT_DATA['version']
    assert project.description == PROJECT_DATA['description']
    assert project.variables[0].key == PROJECT_DATA['variables'][0]['key']
    assert project.variables[0].type == PROJECT_DATA['variables'][0]['type']
    assert project.variables[0].name == PROJECT_DATA['variables'][0]['name']
    assert project.variables[0].description == PROJECT_DATA['variables'][0]['description']
    assert isinstance(project.variables[0].value, PolygonFeatureCollection)
    assert project.variables[1].key == PROJECT_DATA['variables'][1]['key']
    assert project.variables[1].type == PROJECT_DATA['variables'][1]['type']
    assert project.variables[1].name == PROJECT_DATA['variables'][1]['name']
    assert project.variables[1].description == PROJECT_DATA['variables'][1]['description']
    assert isinstance(project.variables[1].value, DataRangeValueVariable)
    assert project.exec_parameters.scale == PROJECT_DATA['exec_parameters']['scale']