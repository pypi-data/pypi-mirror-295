RUN_LAYER = {
    'type': 'test_type',
    'name': 'test_name',
    'time_periods': [
        {
            'mapURL': 'test_mapURL',
            'label': 'test_label',
            'thumbnailURL': 'test_thumbnailURL'
        }
    ],
    'bbox': {
        'SW': [0, 0],
        'NE': [1, 1]
    },
    'legend': {
        'type': 'test_type',
        'values': [
            {
                'test_key': 'test_value'
            }
        ]
    }
}

AUTH_TOKEN_DATA = {
    'token': 'test_token',
    'expires': '2021-01-01T00:00:00'
}

OAUTH_CLIENT_DATA = {
    'name': 'test_name',
    'description': 'test_description',
    'client_id': 'test_client_id',
    'client_secret': 'test_client_secret',
    'enabled': True
}

TABLE_OUTPUT = {
            "title": "Table 1",
            "type": "Table",
            "df": [
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Trees",
                    "Area (ha) within AOI": 120.87512656249999
                },
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Grassland",
                    "Area (ha) within AOI": 152.06326679687493
                },
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Built-up",
                    "Area (ha) within AOI": 284.63527148437487
                },
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Barren / sparse veg",
                    "Area (ha) within AOI": 7.79912421875
                },
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Open water",
                    "Area (ha) within AOI": 198.82971249999989
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Trees",
                    "Area (ha) within AOI": 140.368473828125
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Grassland",
                    "Area (ha) within AOI": 113.06669570312502
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Built-up",
                    "Area (ha) within AOI": 308.0364429687497
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Barren / sparse veg",
                    "Area (ha) within AOI": 3.8994671875
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Open water",
                    "Area (ha) within AOI": 198.8314218749999
                }
            ],
            "resolution": 197.49,
            "figure": None
        }
CHART_OUTPUT = {
            "title": "Table 1 Bar Chart",
            "type": "Chart",
            "df": [
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Trees",
                    "Area (ha) within AOI": 120.87512656249999
                },
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Grassland",
                    "Area (ha) within AOI": 152.06326679687493
                },
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Built-up",
                    "Area (ha) within AOI": 284.63527148437487
                },
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Barren / sparse veg",
                    "Area (ha) within AOI": 7.79912421875
                },
                {
                    "ESA WorldCover (10m) Date": "2020",
                    "ESA WorldCover (10m) Value": "Open water",
                    "Area (ha) within AOI": 198.82971249999989
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Trees",
                    "Area (ha) within AOI": 140.368473828125
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Grassland",
                    "Area (ha) within AOI": 113.06669570312502
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Built-up",
                    "Area (ha) within AOI": 308.0364429687497
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Barren / sparse veg",
                    "Area (ha) within AOI": 3.8994671875
                },
                {
                    "ESA WorldCover (10m) Date": "2021",
                    "ESA WorldCover (10m) Value": "Open water",
                    "Area (ha) within AOI": 198.8314218749999
                }
            ],
            "resolution": None,
            "figure": {
                "data": [
                    {
                        "alignmentgroup": "True",
                        "hovertemplate": "ESA WorldCover (10m) Value=Trees<br>ESA WorldCover (10m) Date=%{x}<br>Area (ha) within AOI=%{y}<extra></extra>",
                        "legendgroup": "Trees",
                        "marker": {
                            "color": "#006400",
                            "pattern": {
                                "shape": ""
                            }
                        },
                        "name": "Trees",
                        "offsetgroup": "Trees",
                        "orientation": "v",
                        "showlegend": True,
                        "textposition": "auto",
                        "x": [
                            "2020",
                            "2021"
                        ],
                        "xaxis": "x",
                        "y": [
                            120.87512656249999,
                            140.368473828125
                        ],
                        "yaxis": "y",
                        "type": "bar"
                    },
                    {
                        "alignmentgroup": "True",
                        "hovertemplate": "ESA WorldCover (10m) Value=Grassland<br>ESA WorldCover (10m) Date=%{x}<br>Area (ha) within AOI=%{y}<extra></extra>",
                        "legendgroup": "Grassland",
                        "marker": {
                            "color": "#ffff4c",
                            "pattern": {
                                "shape": ""
                            }
                        },
                        "name": "Grassland",
                        "offsetgroup": "Grassland",
                        "orientation": "v",
                        "showlegend": True,
                        "textposition": "auto",
                        "x": [
                            "2020",
                            "2021"
                        ],
                        "xaxis": "x",
                        "y": [
                            152.06326679687493,
                            113.06669570312502
                        ],
                        "yaxis": "y",
                        "type": "bar"
                    },
                    {
                        "alignmentgroup": "True",
                        "hovertemplate": "ESA WorldCover (10m) Value=Built-up<br>ESA WorldCover (10m) Date=%{x}<br>Area (ha) within AOI=%{y}<extra></extra>",
                        "legendgroup": "Built-up",
                        "marker": {
                            "color": "#fa0000",
                            "pattern": {
                                "shape": ""
                            }
                        },
                        "name": "Built-up",
                        "offsetgroup": "Built-up",
                        "orientation": "v",
                        "showlegend": True,
                        "textposition": "auto",
                        "x": [
                            "2020",
                            "2021"
                        ],
                        "xaxis": "x",
                        "y": [
                            284.63527148437487,
                            308.0364429687497
                        ],
                        "yaxis": "y",
                        "type": "bar"
                    },
                    {
                        "alignmentgroup": "True",
                        "hovertemplate": "ESA WorldCover (10m) Value=Barren / sparse veg<br>ESA WorldCover (10m) Date=%{x}<br>Area (ha) within AOI=%{y}<extra></extra>",
                        "legendgroup": "Barren / sparse veg",
                        "marker": {
                            "color": "#b4b4b4",
                            "pattern": {
                                "shape": ""
                            }
                        },
                        "name": "Barren / sparse veg",
                        "offsetgroup": "Barren / sparse veg",
                        "orientation": "v",
                        "showlegend": True,
                        "textposition": "auto",
                        "x": [
                            "2020",
                            "2021"
                        ],
                        "xaxis": "x",
                        "y": [
                            7.79912421875,
                            3.8994671875
                        ],
                        "yaxis": "y",
                        "type": "bar"
                    },
                    {
                        "alignmentgroup": "True",
                        "hovertemplate": "ESA WorldCover (10m) Value=Open water<br>ESA WorldCover (10m) Date=%{x}<br>Area (ha) within AOI=%{y}<extra></extra>",
                        "legendgroup": "Open water",
                        "marker": {
                            "color": "#0064c8",
                            "pattern": {
                                "shape": ""
                            }
                        },
                        "name": "Open water",
                        "offsetgroup": "Open water",
                        "orientation": "v",
                        "showlegend": True,
                        "textposition": "auto",
                        "x": [
                            "2020",
                            "2021"
                        ],
                        "xaxis": "x",
                        "y": [
                            198.82971249999989,
                            198.8314218749999
                        ],
                        "yaxis": "y",
                        "type": "bar"
                    }
                ],
                "layout": {
                    "template": {
                        "data": {
                            "histogram2dcontour": [
                                {
                                    "type": "histogram2dcontour",
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ]
                                }
                            ],
                            "choropleth": [
                                {
                                    "type": "choropleth",
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    }
                                }
                            ],
                            "histogram2d": [
                                {
                                    "type": "histogram2d",
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ]
                                }
                            ],
                            "heatmap": [
                                {
                                    "type": "heatmap",
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ]
                                }
                            ],
                            "heatmapgl": [
                                {
                                    "type": "heatmapgl",
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ]
                                }
                            ],
                            "contourcarpet": [
                                {
                                    "type": "contourcarpet",
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    }
                                }
                            ],
                            "contour": [
                                {
                                    "type": "contour",
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ]
                                }
                            ],
                            "surface": [
                                {
                                    "type": "surface",
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ]
                                }
                            ],
                            "mesh3d": [
                                {
                                    "type": "mesh3d",
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    }
                                }
                            ],
                            "scatter": [
                                {
                                    "fillpattern": {
                                        "fillmode": "overlay",
                                        "size": 10,
                                        "solidity": 0.2
                                    },
                                    "type": "scatter"
                                }
                            ],
                            "parcoords": [
                                {
                                    "type": "parcoords",
                                    "line": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    }
                                }
                            ],
                            "scatterpolargl": [
                                {
                                    "type": "scatterpolargl",
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    }
                                }
                            ],
                            "bar": [
                                {
                                    "error_x": {
                                        "color": "#2a3f5f"
                                    },
                                    "error_y": {
                                        "color": "#2a3f5f"
                                    },
                                    "marker": {
                                        "line": {
                                            "color": "#E5ECF6",
                                            "width": 0.5
                                        },
                                        "pattern": {
                                            "fillmode": "overlay",
                                            "size": 10,
                                            "solidity": 0.2
                                        }
                                    },
                                    "type": "bar"
                                }
                            ],
                            "scattergeo": [
                                {
                                    "type": "scattergeo",
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    }
                                }
                            ],
                            "scatterpolar": [
                                {
                                    "type": "scatterpolar",
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    }
                                }
                            ],
                            "histogram": [
                                {
                                    "marker": {
                                        "pattern": {
                                            "fillmode": "overlay",
                                            "size": 10,
                                            "solidity": 0.2
                                        }
                                    },
                                    "type": "histogram"
                                }
                            ],
                            "scattergl": [
                                {
                                    "type": "scattergl",
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    }
                                }
                            ],
                            "scatter3d": [
                                {
                                    "type": "scatter3d",
                                    "line": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    }
                                }
                            ],
                            "scattermapbox": [
                                {
                                    "type": "scattermapbox",
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    }
                                }
                            ],
                            "scatterternary": [
                                {
                                    "type": "scatterternary",
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    }
                                }
                            ],
                            "scattercarpet": [
                                {
                                    "type": "scattercarpet",
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    }
                                }
                            ],
                            "carpet": [
                                {
                                    "aaxis": {
                                        "endlinecolor": "#2a3f5f",
                                        "gridcolor": "white",
                                        "linecolor": "white",
                                        "minorgridcolor": "white",
                                        "startlinecolor": "#2a3f5f"
                                    },
                                    "baxis": {
                                        "endlinecolor": "#2a3f5f",
                                        "gridcolor": "white",
                                        "linecolor": "white",
                                        "minorgridcolor": "white",
                                        "startlinecolor": "#2a3f5f"
                                    },
                                    "type": "carpet"
                                }
                            ],
                            "table": [
                                {
                                    "cells": {
                                        "fill": {
                                            "color": "#EBF0F8"
                                        },
                                        "line": {
                                            "color": "white"
                                        }
                                    },
                                    "header": {
                                        "fill": {
                                            "color": "#C8D4E3"
                                        },
                                        "line": {
                                            "color": "white"
                                        }
                                    },
                                    "type": "table"
                                }
                            ],
                            "barpolar": [
                                {
                                    "marker": {
                                        "line": {
                                            "color": "#E5ECF6",
                                            "width": 0.5
                                        },
                                        "pattern": {
                                            "fillmode": "overlay",
                                            "size": 10,
                                            "solidity": 0.2
                                        }
                                    },
                                    "type": "barpolar"
                                }
                            ],
                            "pie": [
                                {
                                    "automargin": True,
                                    "type": "pie"
                                }
                            ]
                        },
                        "layout": {
                            "autotypenumbers": "strict",
                            "colorway": [
                                "#636efa",
                                "#EF553B",
                                "#00cc96",
                                "#ab63fa",
                                "#FFA15A",
                                "#19d3f3",
                                "#FF6692",
                                "#B6E880",
                                "#FF97FF",
                                "#FECB52"
                            ],
                            "font": {
                                "color": "#2a3f5f"
                            },
                            "hovermode": "closest",
                            "hoverlabel": {
                                "align": "left"
                            },
                            "paper_bgcolor": "white",
                            "plot_bgcolor": "#E5ECF6",
                            "polar": {
                                "bgcolor": "#E5ECF6",
                                "angularaxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                },
                                "radialaxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                }
                            },
                            "ternary": {
                                "bgcolor": "#E5ECF6",
                                "aaxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                },
                                "baxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                },
                                "caxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                }
                            },
                            "coloraxis": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "colorscale": {
                                "sequential": [
                                    [
                                        0.0,
                                        "#0d0887"
                                    ],
                                    [
                                        0.1111111111111111,
                                        "#46039f"
                                    ],
                                    [
                                        0.2222222222222222,
                                        "#7201a8"
                                    ],
                                    [
                                        0.3333333333333333,
                                        "#9c179e"
                                    ],
                                    [
                                        0.4444444444444444,
                                        "#bd3786"
                                    ],
                                    [
                                        0.5555555555555556,
                                        "#d8576b"
                                    ],
                                    [
                                        0.6666666666666666,
                                        "#ed7953"
                                    ],
                                    [
                                        0.7777777777777778,
                                        "#fb9f3a"
                                    ],
                                    [
                                        0.8888888888888888,
                                        "#fdca26"
                                    ],
                                    [
                                        1.0,
                                        "#f0f921"
                                    ]
                                ],
                                "sequentialminus": [
                                    [
                                        0.0,
                                        "#0d0887"
                                    ],
                                    [
                                        0.1111111111111111,
                                        "#46039f"
                                    ],
                                    [
                                        0.2222222222222222,
                                        "#7201a8"
                                    ],
                                    [
                                        0.3333333333333333,
                                        "#9c179e"
                                    ],
                                    [
                                        0.4444444444444444,
                                        "#bd3786"
                                    ],
                                    [
                                        0.5555555555555556,
                                        "#d8576b"
                                    ],
                                    [
                                        0.6666666666666666,
                                        "#ed7953"
                                    ],
                                    [
                                        0.7777777777777778,
                                        "#fb9f3a"
                                    ],
                                    [
                                        0.8888888888888888,
                                        "#fdca26"
                                    ],
                                    [
                                        1.0,
                                        "#f0f921"
                                    ]
                                ],
                                "diverging": [
                                    [
                                        0,
                                        "#8e0152"
                                    ],
                                    [
                                        0.1,
                                        "#c51b7d"
                                    ],
                                    [
                                        0.2,
                                        "#de77ae"
                                    ],
                                    [
                                        0.3,
                                        "#f1b6da"
                                    ],
                                    [
                                        0.4,
                                        "#fde0ef"
                                    ],
                                    [
                                        0.5,
                                        "#f7f7f7"
                                    ],
                                    [
                                        0.6,
                                        "#e6f5d0"
                                    ],
                                    [
                                        0.7,
                                        "#b8e186"
                                    ],
                                    [
                                        0.8,
                                        "#7fbc41"
                                    ],
                                    [
                                        0.9,
                                        "#4d9221"
                                    ],
                                    [
                                        1,
                                        "#276419"
                                    ]
                                ]
                            },
                            "xaxis": {
                                "gridcolor": "white",
                                "linecolor": "white",
                                "ticks": "",
                                "title": {
                                    "standoff": 15
                                },
                                "zerolinecolor": "white",
                                "automargin": True,
                                "zerolinewidth": 2
                            },
                            "yaxis": {
                                "gridcolor": "white",
                                "linecolor": "white",
                                "ticks": "",
                                "title": {
                                    "standoff": 15
                                },
                                "zerolinecolor": "white",
                                "automargin": True,
                                "zerolinewidth": 2
                            },
                            "scene": {
                                "xaxis": {
                                    "backgroundcolor": "#E5ECF6",
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "showbackground": True,
                                    "ticks": "",
                                    "zerolinecolor": "white",
                                    "gridwidth": 2
                                },
                                "yaxis": {
                                    "backgroundcolor": "#E5ECF6",
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "showbackground": True,
                                    "ticks": "",
                                    "zerolinecolor": "white",
                                    "gridwidth": 2
                                },
                                "zaxis": {
                                    "backgroundcolor": "#E5ECF6",
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "showbackground": True,
                                    "ticks": "",
                                    "zerolinecolor": "white",
                                    "gridwidth": 2
                                }
                            },
                            "shapedefaults": {
                                "line": {
                                    "color": "#2a3f5f"
                                }
                            },
                            "annotationdefaults": {
                                "arrowcolor": "#2a3f5f",
                                "arrowhead": 0,
                                "arrowwidth": 1
                            },
                            "geo": {
                                "bgcolor": "white",
                                "landcolor": "#E5ECF6",
                                "subunitcolor": "white",
                                "showland": True,
                                "showlakes": True,
                                "lakecolor": "white"
                            },
                            "title": {
                                "x": 0.05
                            },
                            "mapbox": {
                                "style": "light"
                            }
                        }
                    },
                    "xaxis": {
                        "anchor": "y",
                        "domain": [
                            0.0,
                            1.0
                        ],
                        "title": {
                            "text": "ESA WorldCover (10m) Date"
                        }
                    },
                    "yaxis": {
                        "anchor": "x",
                        "domain": [
                            0.0,
                            1.0
                        ],
                        "title": {
                            "text": "Area (ha) within AOI"
                        }
                    },
                    "legend": {
                        "title": {
                            "text": "ESA WorldCover (10m) Value",
                            "side": "top"
                        },
                        "tracegroupgap": 0,
                        "font": {
                            "family": "Montserrat, sans-serif",
                            "color": "#373737"
                        },
                        "orientation": "h",
                        "yanchor": "top",
                        "xanchor": "left",
                        "y": 1.15
                    },
                    "margin": {
                        "t": 60
                    },
                    "barmode": "group",
                    "plot_bgcolor": "#f3f3f3",
                    "font": {
                        "family": "Montserrat, sans-serif",
                        "color": "#373737"
                    },
                    "height": 700
                }
            }
        }


PROJECT_DATA = {
            "id": "oCNCgZ8R2ZutC02pMvVC",
            "title": "VariablesTest",
            "version": "1.0.0",
            "description": "A simple workflow to test the variables are working in the API",
            "variables": [
                {
                    "key": "var_1",
                    "type": "area",
                    "name": "Study Area",
                    "description": "The study area to create a S2 Composite over",
                    "value": {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "geometry": {
                                    "type": "Polygon",
                                    "coordinates": [
                                        [
                                            [
                                                0.283130166960186,
                                                51.46855955964676
                                            ],
                                            [
                                                0.268023965788311,
                                                51.46855955964676
                                            ],
                                            [
                                                0.268023965788311,
                                                51.45016295941291
                                            ],
                                            [
                                                0.283130166960186,
                                                51.45016295941291
                                            ],
                                            [
                                                0.283130166960186,
                                                51.46855955964676
                                            ]
                                        ]
                                    ]
                                },
                                "properties": {}
                            }
                        ]
                    }
                },
                {
                    "key": "var_2",
                    "type": "date range",
                    "name": "Study Period",
                    "description": "",
                    "value": {
                        "start_date": "2020-01-01T00:00:00",
                        "end_date": "2021-12-31T00:00:00"
                    }
                }
            ],
            "exec_parameters": {
                "scale": 10,
            }
        }


POINT = '[26.665387423985948,5.909387121827919]'
POLYGON = '[[[26.629758489241198,5.331277894260012],[26.629758489241198,4.916017753856224],[26.980218851583544,4.916017753856224],[26.980218851583544,5.331277894260012],[26.629758489241198,5.331277894260012]]]'

POINT_FEATURE = '{"type": "Feature","properties": {},"geometry": {"coordinates": '+POINT+', "type": "Point"}}'
POINT_FEATURE_COLLECTION = '{"type": "FeatureCollection","features": [' + POINT_FEATURE + ']}'

POLYGON_FEATURE = '{"type": "Feature","properties": {},"geometry": {"coordinates": '+POLYGON+',"type": "Polygon"}}'
POLYGON_FEATURE_COLLECTION = '{"type": "FeatureCollection","features": [' + POLYGON_FEATURE + ']}'

MULITPOINT_FEATURE = '{"type": "Feature","properties": {},"geometry": {"coordinates": ['+POINT+'],' + '"type": "MultiPoint"}}'
MULTIPOLYGON_FEATURE = '{"type": "Feature","properties": {},"geometry": {"coordinates": ['+POLYGON+'],' + '"type": "MultiPolygon"}}'


RUN = {
    "status": "completed",
    "id": "f2a8ce6fca86497287732b957c0d9b2f",
    "started_at": "2024-09-06T13:31:37.170000Z",
    "completed_at": "2024-09-06T13:32:01.850679Z",
    "exec_parameters": {
        "max_pixels": 10000000000000,
        "scale": 250,
        "best_effort": True
    },
    "variables": [],
    "layers": [RUN_LAYER],
    "outputs": [TABLE_OUTPUT, CHART_OUTPUT]
}