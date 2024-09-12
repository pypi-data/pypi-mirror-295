"""Defines an output from earth blox."""

"""
----------------------------------------------------------------------------
COMMERCIAL IN CONFIDENCE

(c) Copyright Quosient Ltd. All Rights Reserved.

See LICENSE.txt in the repository root.
----------------------------------------------------------------------------
"""
import pandas as pd
from plotly import graph_objects as go
from plotly.io import from_json
from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
import json

def validate_to_df(df):
    if df is not None and not isinstance(df, pd.DataFrame):
        return pd.DataFrame.from_records(df)
    return df

def validate_to_figure(figure):
    if figure is not None and not isinstance(figure, go.Figure):
        return from_json(json.dumps(figure))
    return figure

class Output(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """The config for the model."""
    
    title: str
    """The title of the output."""

    type: str
    """The type of output."""

    df: Annotated[Optional[pd.DataFrame], BeforeValidator(validate_to_df)] = None
    """The dataframe of the output, input as a dictionary."""

    resolution: Optional[float] = None
    """The resolution of the output in metres."""

    figure: Annotated[Optional[go.Figure], BeforeValidator(validate_to_figure)] = None
    """The figure of the output."""

    def show_figure(self):
        """Show the figure."""        
        if self.figure is None:
            raise ValueError("No figure to show.")

        self.figure.show()

    def get_dataframe(self):
        """Get the dataframe."""
        if self.df is None:
            raise ValueError("No dataframe")
        
        return self.df