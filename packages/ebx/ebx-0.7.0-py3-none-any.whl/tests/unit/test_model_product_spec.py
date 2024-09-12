from ebx.models.project_spec import ProjectSpec
import pytest

def test_can_set_basic_product_spec():
    data = {
        'project_id': 'test_product_id',
        'type': 'template'
    }
    spec = ProjectSpec(**data)

    assert spec.project_id == data['project_id']
    assert spec.type == data['type']
    assert spec.get_project_id() == 'test_product_id'


def test_can_set_href_product_spec():
    data = {
        'href': 'some/path/to/project_id',
        'type': 'href_template'
    }
    spec = ProjectSpec(**data)

    assert spec.href == data['href']
    assert spec.type == data['type']
    assert spec.get_project_id() == 'project_id'

def test_cannot_set_project_id_with_href():
    data = {
        'project_id': 'test_product_id',
        'href': 'some/path/to/project_id',
        'type': 'href_template'
    }
    with pytest.raises(ValueError):
        ProjectSpec(**data)


def test_cannot_set_project_id_with_href_type():
    data = {
        'project_id': 'test_product_id',
        'type': 'href_template'
    }
    with pytest.raises(ValueError):
        ProjectSpec(**data)

def test_cannot_set_href_with_template_type():
    data = {
        'href': 'some/path/to/project_id',
        'type': 'template'
    }
    with pytest.raises(ValueError):
        ProjectSpec(**data)