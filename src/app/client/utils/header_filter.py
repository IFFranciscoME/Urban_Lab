import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app.dash import app
from config.config import name


header_filter = html.Header(
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
                                className='m-auto text-primary font-weight-bold d-none d-md-block d-lg-block d-xl-block text-center text-justify' )
                        ], className='d-flex flex-row')
                    ], className='col-3 col-sm-3 col-md-8 col-lg-8 col-xl-8 mx-auto'),
                ], 
                className='row w-100 m-0 p-0 d-flex justify-content-center align-items-center',
                style={'height':'80px'})
            ], className='container-fluid m-0 p-0'),
            className='navbar navbar-white bg-white m-0 p-0'
        )
    ],
    className='sticky-top bg-white w-100 border-bottom')
