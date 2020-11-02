import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app.dash import app
from config.config import name


header = html.Header(
    children=[
        dbc.Nav(
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Img(
                                src=app.get_asset_url('logo.png'),
                                height='60px',
                                className='mr-3'),
                            html.H2(
                                name,
                                className='m-auto text-primary font-weight-bold d-none d-md-block d-lg-block d-xl-block text-center text-justify'),
                            html.A(dbc.Button("Filtros", id="buttonfilter", className="mr-1", style={'background': '#317CF6', 'height': 40, 'margin-top': 10}), href="/filterEconomic")
                        ], className='d-flex flex-row')
                    ], className='col-3 col-sm-3 col-md-8 col-lg-8 col-xl-8 mx-auto'),
                    html.Div([

                        dcc.Dropdown(
                            id='slct_map',
                            options=[
                                {'label': 'Estrés Económico',
                                    'value': 'Estres'},
                                {'label': 'Adaptabilidad',
                                    'value': 'Adaptabilidad'},
                                {'label': 'Predicción de Precios',
                                    'value': 'Precios'}
                            ],
                            multi=False,
                            clearable=False,
                            value='Estres',
                            style={
                                'color': '#272E42',
                                'background-color': '#D1D8EE',
                                'fontSize': '20px'
                            },
                            className='w-100 h-100 m-auto')
                    ], className='col-9 col-sm-9 col-md-4 col-lg-4 col-xl-4 mx-auto')
                ], 
                className='row w-100 m-0 p-0 d-flex justify-content-center align-items-center',
                style={'height':'80px'})
            ], className='container-fluid m-0 p-0'),
            className='navbar navbar-white bg-white m-0 p-0'
        )
    ],
    className='sticky-top bg-white w-100 border-bottom')
