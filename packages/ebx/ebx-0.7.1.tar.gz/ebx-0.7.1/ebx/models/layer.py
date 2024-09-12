"""Defines a layer from earth blox."""

"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
from typing import List, Optional
from pydantic import BaseModel

class LayerTimePeriod(BaseModel):
    """Layer groups containing map urls, labels and thumbnails."""
    mapURL: str
    label: str
    thumbnailURL: Optional[str] = None

class Bounds(BaseModel):
    """Defines a bounding box."""
    SW: List[float]
    NE: List[float]

class Legend(BaseModel):
    """Defines a legend for a layer."""
    type: str
    values: List[dict]

class Layer(BaseModel):
    """Defines a layer from earth blox."""
    type: str
    name: str
    time_periods: List[LayerTimePeriod]
    bbox: Bounds
    legend: Optional[Legend] = None
