"""Class defining the result of a run."""

"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""

import leafmap.leafmap as leafmap
from typing import List, Optional
from ebx.models.output import Output
from ebx.models.layer import Layer
from .variables import VariableConfig
from .exec_parameters import Config
from pydantic import BaseModel
from datetime import datetime

# TODO: create run by id and add api methods to run
class Run(BaseModel):
    """Describes a run."""
    status: str
    """The status of the run."""

    id: str
    """The id of the run."""

    started_at: Optional[datetime] = None
    """The time the run started."""

    completed_at: Optional[datetime] = None
    """The time the run completed."""

    variables: Optional[List[VariableConfig]] = []
    """The variables associated with the project."""

    exec_parameters: Optional[Config] = None
    """The execution parameters associated with the project."""

    layers: Optional[list] = None
    """The layers associated with the run."""

    outputs: Optional[list] = None
    """The outputs associated with the run."""

    def add_legends_to_map(self, map):
        raise NotImplementedError

    def add_layers_to_map(self, map):
        """For each layer, add the layer to the map."""
        layer_urls = []
        layer_labels = []

        for layer in self.layers:
            if 'time_periods' in layer and layer['time_periods'] is not None:
                for group in layer['time_periods']:
                    layer_urls.append(group['mapURL'])
                    layer_labels.append(group['label'])

        for url, label in zip(layer_urls, layer_labels):
            map.add_tile_layer(url, name=label, attribution="Earth Blox")

    def get_bounding_box(self) -> list:
        """Get the bounding box of the run."""
        all_bounds = [layer['bbox'] for layer in self.layers]

        min_lat = min([bounds['SW'][0] for bounds in all_bounds])
        min_lon = min([bounds['SW'][1] for bounds in all_bounds])
        max_lat = max([bounds['NE'][0] for bounds in all_bounds])
        max_lon = max([bounds['NE'][1] for bounds in all_bounds])

        return [[min_lat, min_lon], [max_lat, max_lon]]
    
    def plot(self) -> leafmap.Map:
        """Returns a leafmap map with the layers"""
        m = leafmap.Map()

        self.add_layers_to_map(m)
        
        m.fit_bounds(self.get_bounding_box())

        return m
    
    def get_layers(self) -> List[Layer]:
        """Returns the layers of the run."""

        if self.layers is None:
            return []

        return [Layer(**layer) for layer in self.layers]
    
    def get_outputs(self) -> List[Output]:
        """Returns the outputs of the run."""

        if self.outputs is None:
            return []

        return [Output(**output) for output in self.outputs]