from ebx.models.output import Output
import pandas as pd
from plotly import graph_objects as go
from .constants import TABLE_OUTPUT, CHART_OUTPUT

def test_table_output_can_load():
    client = Output(**TABLE_OUTPUT)
    assert client.title == TABLE_OUTPUT['title']
    assert client.type == TABLE_OUTPUT['type']
    assert client.get_dataframe().shape == (10,3)
    assert isinstance(client.get_dataframe(), pd.DataFrame)


def test_chart_output_can_load():
    client = Output(**CHART_OUTPUT)
    assert client.title == CHART_OUTPUT['title']
    assert client.type == CHART_OUTPUT['type']
    assert client.figure is not None
    assert isinstance(client.figure, go.Figure)

    