from ebx.models.run import Run
from .constants import RUN, RUN_LAYER
import leafmap.leafmap as leafmap

def test_can_load_run():
    run = Run(**RUN)

    assert run.id == RUN['id']
    assert run.status == RUN['status']
    assert run.started_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == RUN['started_at']
    assert run.completed_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == RUN['completed_at']

    assert len(run.get_layers()) == 1
    assert len(run.get_outputs()) == 2


def test_can_get_bounding_box():
    run = Run(**RUN)

    bbox = run.get_bounding_box()
    assert bbox[0] == RUN_LAYER['bbox']['SW']
    assert bbox[1] == RUN_LAYER['bbox']['NE']

def test_can_plot():
    run = Run(**RUN)
    assert isinstance(run.plot(),leafmap.Map)