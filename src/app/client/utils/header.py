import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app.dash import app
from config.config import name
from dash.dependencies import Input, Output, State, MATCH



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
                            dbc.Button("Levantar Datos", {"index": 1, "role": "open"}, className="mr-1", style={'background': '#317CF6', 'height': 40, 'margin-top': 10}),
                            html.Div(dbc.Modal(
                                    [
                                    dbc.ModalHeader(
                                        children=[
                                            html.H3("Bienvenido a la herramienta de levantamiento de datos"),
                                            html.H5("Apoyanos contestando las siguientes preguntas, con el fin de agregar información a nuestra bas de datos")
                                        ],
                                        className='text-center text-justify'
                                    ),
                                    dbc.ModalBody(
                                        children=[
                                            dbc.Form([
                                            dbc.FormGroup([
                                                dbc.Label("Seleccione el sector en el que opera su empresa:"),
                                                html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'Manufactura', 'value': 'Manufactura'},
                                                        {'label': 'Comercio', 'value': 'Comercio'},
                                                        {'label': 'Servicio', 'value': 'Servicio'},
                                                        {'label': 'Construcción', 'value': 'Construcción'},
                                                    ]
                                                    ),
                                                        ]),
                                                html.Br(),
                                            dbc.FormGroup([
                                                dbc.Label("¿Cuál ha sido el comportamiento de sus ventas del trimestre actual respecto al anterior?"),
                                                html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'Se mantuvieron igual', 'value': 'Se mantuvieron igual'},
                                                        {'label': 'Se han reducido', 'value': 'Se han reducido'},
                                                        {'label': 'Se han aumentado', 'value': 'Se han aumentado'}
                                                    ]
                                                    ),
                                                ]),
                                                html.Br(),
                                            dbc.FormGroup([
                                                dbc.Label("¿Cuál ha sido el comportamiento de sus  costos operativos?"),
                                                html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'Se mantuvieron igual', 'value': 'Se mantuvieron igual'},
                                                        {'label': 'Se han reducido', 'value': 'Se han reducido'},
                                                        {'label': 'Se han aumentado', 'value': 'Se han aumentado'}
                                                    ],
                                                    ),
                                                ]),
                                                html.Br(),
                                            dbc.FormGroup([
                                                dbc.Label("En el supuesto de no generar ventas en el futuro, ¿Cuántas semanas soportarían sus fondos para pagar todos sus gastos?"),
                                                html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': '0 a 6 semanas', 'value': '1'},
                                                        {'label': '6 a 12 semanas', 'value': '2'},
                                                        {'label': '12 a 18 semanas', 'value': '3'},
                                                        {'label': '18 a 24 semanas o más', 'value': '4'}
                                                    ],
                                                    ),
                                                ]),
                                                html.Br(),
                                            dbc.FormGroup([
                                                dbc.Label("Indique el porcentaje aproximado de aumento o reducción en ventas del trimestre actual respecto al anterior:"),
                                                html.Br(),
                                                dcc.Slider(min=0, max=100, step=10, value=100,
                                                           marks={
                                                                0: {'label': '0%'},
                                                                10: {'label': '10%'},
                                                                20: {'label': '20%'},
                                                                30: {'label': '30%'},
                                                                40: {'label': '40%'},
                                                                50: {'label': '50%'},
                                                                60: {'label': '60%'},
                                                                70: {'label': '70%'},
                                                                80: {'label': '80%'},
                                                                90: {'label': '90%'},
                                                                100: {'label': '100%'},

                                                             }
                                                           )


                                            ]
                                            )
                                        ])

                                            ],
                                        className='text-center text-justify'
                                    ),
                                    dbc.ModalFooter(
                                        dbc.Button([
                                            'Enviar'
                                        ],
                                            id={"index": 1, "role": "close"},
                                            className='m-auto btn btn-success'
                                        )
                                    ),
                                ],
                                id = {"index": 1, "role": "modal"},
                                centered = True,
                                autoFocus = True,
                                scrollable=True,
                                backdrop="static"

                            ))
                        ],
                            className='d-flex flex-row',
                        )
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
                                    'value': 'Precios'},
                                {'label': 'Filtros de búsqueda',
                                 'value': 'Filtros'}
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



@app.callback(
    Output({'index': MATCH, 'role': 'modal'}, 'is_open'),
    [
        Input({'index': MATCH, 'role': 'open'}, 'n_clicks'),
        Input({'index': MATCH, 'role': 'close'}, 'n_clicks')
    ],
    [State({'index': MATCH, 'role': 'modal'}, 'is_open')],
)
def toggle_modal_barchart(n1, n2, is_open):

    if n1 or n2:
        return not is_open
    return is_open
