import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app.client.components.graphics1 import tabs_barchart1, tabs_barchart2, map_graphP1, map_graphP2, map_graphBars
from model.filter_graphics import optionslct
#from model.filter_graphics import test

municipio = optionslct('Municipio')
giro = optionslct('Giro')

body_filter = html.Div([
    html.Div([
        html.Div([
                dbc.Card(
                    [
                        
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
                        html.Div([
                            html.H5(children='Sector:', id="sectortxt", className='text-justify'),
                            dcc.Dropdown(
                                id='sectorSlct',
                                options=[
                                    {'label':'Manufactura',
                                    'value': 'Manufactura'},
                                    {'label': 'Servicios',
                                    'value': 'Servicios'},
                                    {'label':'Construcción',
                                    'value': 'Construcción'},
                                    {'label':'Comercio',
                                    'value': 'Comercio'},
                                ],
                                multi=False,
                                clearable=False,
                                value= "Servicios",
                                style={
                                'color': '#272E42',
                                'background-color': '#D1D8EE',
                                'fontSize': '20px'
                                },
                                className='w-100 h-100'
                            ),
                            dcc.Checklist(
                                id="sectorcheck",
                                options=[{"label": "No me interesa",
                                          "value": "X"}]
                            )
                    ], className='w-50 h-100'),
                        html.Div([
                            html.H5(children='Giro:', id="girotxt", className='text-justify'),
                            dcc.Dropdown(
                                id='giroSlct',
                                options=[
                                    {'label': name,
                                     'value': name} for name in giro
                                ],
                                multi=False,
                                clearable=False,
                                value="Restaurantes",
                                style={
                                    'color': '#272E42',
                                    'background-color': '#D1D8EE',
                                    'fontSize': '20px'
                                },
                                className='w-100 h-100'
                            ),
                            dcc.Checklist(
                                id="girocheck",
                                options=[{"label": "No me interesa",
                                          "value": "X"}]
                            )
                        ], className='w-50 h-100'),
                        html.Div([
                            html.H5(children='Municipio:', id="municipiotxt", className='text-justify'),
                            dcc.Dropdown(
                                id='municipioSlct',
                                options=[
                                    {'label': name,
                                     'value': name} for name in municipio
                                ],
                                multi=False,
                                clearable=False,
                                value="Guadalajara",
                                style={
                                    'color': '#272E42',
                                    'background-color': '#D1D8EE',
                                    'fontSize': '20px'
                                },
                                className='w-100 h-100'
                            ),
                            dcc.Checklist(
                                id="municipiocheck",
                                options=[{"label": "No me interesa",
                                          "value": "X"}]
                            )
                        ], className='w-50 h-100')
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
                    tabs_barchart1
                ]),
                map_graphP1
            ],
                body=True,
                className='card h-100',
                style={'backgroundColor': '#F9F9F9'})
        ], className='col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6  mt-3')
    ], className='row'),
    html.Div([
        html.Div([
            dbc.Card([
                map_graphBars
            ],
                body=True,
                className='card h-100',
                style={'backgroundColor': '#F9F9F9'})
        ], className='col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6  mt-3'),
        html.Div([
            dbc.Card([
                html.Div([
                    tabs_barchart2
                ]),
                map_graphP2
            ],
                body=True,
                className='card h-100',
                style={'backgroundColor': '#F9F9F9'})
        ], className='col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6  mt-3')
    ], className='row'),
], className='container-fluid mb-auto', style={'backgroundColor': '#F2F2F2'})
