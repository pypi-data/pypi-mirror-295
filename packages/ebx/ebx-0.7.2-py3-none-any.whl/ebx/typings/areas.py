from geojson_pydantic import FeatureCollection, Feature, Polygon, MultiPolygon, Point, MultiPoint
from typing import Dict, Union

# see https://developmentseed.org/geojson-pydantic/intro/#advanced-usage
PolygonFeature = Feature[Polygon, Dict]
"""A feature that only allows polygon geometry."""

PointFeature = Feature[Point, Dict]
"""A feature that only allows point geometry."""

MultiPolygonFeature = Feature[MultiPolygon, Dict]
"""A feature that only allows multi polygon geometry."""

MultiPointFeature = Feature[MultiPoint, Dict]
"""A feature that only allows multi polygon geometry."""

PolygonFeatureCollection = FeatureCollection[Union[PolygonFeature, MultiPolygonFeature]]
"""A feature collection that only allows polygon or multi polygon features."""

PointFeatureCollection = FeatureCollection[Union[PointFeature, MultiPointFeature]]
"""A feature collection that only allows points or multi points features."""

Areas = Union[PolygonFeatureCollection, PolygonFeature, MultiPolygonFeature, PointFeatureCollection, PointFeature, MultiPointFeature]
"""Area is defined as a polygon feature collection, polygon feature or multi polygon feature.

Feature collections are converted to collections of areas and shapes.

Areas are made up of either a single polygon (A polygon feature) or multiple polygons (A multi polygon feature).
"""