from ebx.models.variables.date_range_variable import DateRangeVariable
from datetime import datetime
import pytest

def test_date_variable():
    data = {
        'key': 'var_1',
        'type': 'date range',
        'name': 'test',
        'description': 'test description',
        'value': {
            'start_date': '2021-01-01',
            'end_date': '2022-01-01'
        }
    }

    date = DateRangeVariable(**data)

    assert date.key == data['key']
    assert date.name == data['name']
    assert date.description == data['description']
    assert date.type == 'date range'
    assert isinstance(date.value.start_date, datetime)
    assert isinstance(date.value.end_date, datetime)
    assert date.value.start_date == datetime.strptime(data['value']['start_date'], '%Y-%m-%d')
    assert date.value.end_date == datetime.strptime(data['value']['end_date'], '%Y-%m-%d')


def test_invalid_date_variable():
    data = {
        'key': 'var_1',
        'type': 'date range',
        'name': 'test',
        'description': 'test description',
        'value': 'invalid_date'
    }

    with pytest.raises(ValueError):
        date = DateRangeVariable(**data)


def test_invalid_date_object_variable():
    data = {
        'key': 'var_1',
        'type': 'date range',
        'name': 'test',
        'description': 'test description',
        'value': {}
    }

    with pytest.raises(ValueError):
        date = DateRangeVariable(**data)

def test_invalid_date_object_values_variable():
    data = {
        'key': 'var_1',
        'type': 'date range',
        'name': 'test',
        'description': 'test description',
        'value': {
            'start_date': 'abc1234',
            'end_date': 43133232
        }
    }

    with pytest.raises(ValueError):
        date = DateRangeVariable(**data)