import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app.client.components.map import map_graph, txt_variables
from app.client.components.barchart import barchart, modal_barchart, output_barchart
from app.client.components.treemap import treemap, tabs_barchart

body = html.Div([
    html.Div([
        html.Div([
                dbc.Card(
                    [
                       txt_variables
                    ],
                    body=True,
                    className='card h-100 ',
                    style={'backgroundColor': '#F9F9F9'})
                ],
            className='col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 mt-3',
        )
    ], className='row'),
    html.Div([
        html.Div([
                dbc.Card(
                    [
                        map_graph
                    ],
                    body=True,
                    className='card h-100 ',
                    style={'backgroundColor': '#F9F9F9'})
                ],
            className='col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6 mt-3',
        ),
        html.Div([
            dbc.Card([
                html.Div([
                    output_barchart
                ]),
                barchart
            ],
                body=True,
                className='card h-100',
                style={'backgroundColor': '#F9F9F9'})
        ], className='col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6  mt-3')
    ], className='row'),
    html.Div([
        html.Div([
            dbc.Card([
                tabs_barchart,
                treemap
            ],
                body=True,
                className='card h-100',
                style={'backgroundColor': '#F9F9F9'})
        ], className='col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12  mt-3 mb-3')
    ], className='row'),
    modal_barchart
], className='container-fluid mb-auto', style={'backgroundColor': '#F2F2F2'})
