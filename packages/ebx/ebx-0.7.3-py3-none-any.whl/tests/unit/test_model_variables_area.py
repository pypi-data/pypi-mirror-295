from ebx.models.variables.area_variable import AreaVariable
from ebx.typings.areas import PointFeature, PolygonFeature, MultiPointFeature, MultiPolygonFeature, PointFeatureCollection, PolygonFeatureCollection
import json
from .constants import POINT_FEATURE, POLYGON_FEATURE, MULITPOINT_FEATURE, MULTIPOLYGON_FEATURE, POINT_FEATURE_COLLECTION, POLYGON_FEATURE_COLLECTION


def test_point_feature():
    point_feature = json.loads(POINT_FEATURE)

    data = {
        'key': 'var_1',
        'type': 'area',
        'name': 'test',
        'description': 'test description',
        'value': point_feature
    }

    area = AreaVariable(**data)

    assert area.key == data['key']
    assert area.name == data['name']
    assert area.description == data['description']
    assert area.type == 'area'
    assert isinstance(area.value, PointFeature)


def test_polygon_feature():
    feature = json.loads(POLYGON_FEATURE)

    data = {
        'key': 'var_1',
        'type': 'area',
        'name': 'test',
        'description': 'test description',
        'value': feature
    }

    area = AreaVariable(**data)

    assert area.key == data['key']
    assert area.name == data['name']
    assert area.description == data['description']
    assert area.type == 'area'
    assert isinstance(area.value, PolygonFeature)


def test_multi_point_feature():
    point_feature = json.loads(MULITPOINT_FEATURE)

    data = {
        'key': 'var_1',
        'type': 'area',
        'name': 'test',
        'description': 'test description',
        'value': point_feature
    }

    area = AreaVariable(**data)

    assert area.key == data['key']
    assert area.name == data['name']
    assert area.description == data['description']
    assert area.type == 'area'
    assert isinstance(area.value, MultiPointFeature)


def test_multi_polygon_feature():
    feature = json.loads(MULTIPOLYGON_FEATURE)

    data = {
        'key': 'var_1',
        'type': 'area',
        'name': 'test',
        'description': 'test description',
        'value': feature
    }

    area = AreaVariable(**data)

    assert area.key == data['key']
    assert area.name == data['name']
    assert area.description == data['description']
    assert area.type == 'area'
    assert isinstance(area.value, MultiPolygonFeature)


def test_point_feature_collection():
    point_feature = json.loads(POINT_FEATURE_COLLECTION)

    data = {
        'key': 'var_1',
        'type': 'area',
        'name': 'test',
        'description': 'test description',
        'value': point_feature
    }

    area = AreaVariable(**data)

    assert area.key == data['key']
    assert area.name == data['name']
    assert area.description == data['description']
    assert area.type == 'area'
    assert isinstance(area.value, PointFeatureCollection)


def test_polygon_feature_collection():
    feature = json.loads(POLYGON_FEATURE_COLLECTION)

    data = {
        'key': 'var_1',
        'type': 'area',
        'name': 'test',
        'description': 'test description',
        'value': feature
    }

    area = AreaVariable(**data)

    assert area.key == data['key']
    assert area.name == data['name']
    assert area.description == data['description']
    assert area.type == 'area'
    assert isinstance(area.value, PolygonFeatureCollection)


def test_string():
    data = {
        'key': 'var_1',
        'type': 'area',
        'name': 'test',
        'description': 'test description',
        'value': 'my_asset'
    }

    area = AreaVariable(**data)

    assert area.key == data['key']
    assert area.name == data['name']
    assert area.description == data['description']
    assert area.type == 'area'
    assert area.value == data['value']