from ebx.models.variables.base_variable import BaseVariable
import pytest

def test_key_requirement():
    data = {
        'type': 'date',
        'name': 'test',
        'description': 'test description',
        'value': '2021-01-01'
    }

    with pytest.raises(ValueError):
        variable = BaseVariable(**data)


def test_type_requirement():
    data = {
        'key': 'var_1',
        'name': 'test',
        'description': 'test description',
        'value': '2021-01-01'
    }

    with pytest.raises(ValueError):
        variable = BaseVariable(**data)