import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app.dash import app
from dash.dependencies import Input, Output, State

from app.client.utils.body import body
from app.client.utils.body_filter import body_filter

@app.callback(
    Output(
        component_id='select-body',
        component_property='children'
    ),
    Input(
        component_id='slct_map',
        component_property='value'
    )
)

def changebody(slct):
    if slct == 'Filtros':
        return body_filter
    return body