from ebx.models.variables.date_variable import DateVariable
from datetime import datetime
import pytest

def test_date_variable():
    data = {
        'key': 'var_1',
        'type': 'date',
        'name': 'test',
        'description': 'test description',
        'value': '2021-01-01'
    }

    date = DateVariable(**data)

    assert date.key == data['key']
    assert date.name == data['name']
    assert date.description == data['description']
    assert date.type == 'date'
    assert isinstance(date.value, datetime)
    assert date.value == datetime.strptime(data['value'], '%Y-%m-%d')


def test_invalid_date_variable():
    data = {
        'key': 'var_1',
        'type': 'date',
        'name': 'test',
        'description': 'test description',
        'value': 'invalid_date'
    }

    with pytest.raises(ValueError):
        date = DateVariable(**data)