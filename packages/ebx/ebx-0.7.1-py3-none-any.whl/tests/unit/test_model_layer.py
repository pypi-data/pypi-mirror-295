from ebx.models.layer import Layer
from .constants import RUN_LAYER

def test_layer_can_load():
    layer = Layer(**RUN_LAYER)
    assert layer.type == RUN_LAYER['type']
    assert layer.name == RUN_LAYER['name']
    assert layer.time_periods[0].mapURL == RUN_LAYER['time_periods'][0]['mapURL']
    assert layer.time_periods[0].label == RUN_LAYER['time_periods'][0]['label']
    assert layer.time_periods[0].thumbnailURL == RUN_LAYER['time_periods'][0]['thumbnailURL']
    assert layer.bbox.SW == RUN_LAYER['bbox']['SW']
    assert layer.bbox.NE == RUN_LAYER['bbox']['NE']
    assert layer.legend.type == RUN_LAYER['legend']['type']
    assert layer.legend.values[0] == RUN_LAYER['legend']['values'][0]

    