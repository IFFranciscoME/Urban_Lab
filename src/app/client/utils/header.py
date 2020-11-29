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
                                            html.H5("Apoyanos contestando las siguientes preguntas, con el fin de agregar información a la base de datos colectiva y pública")
                                        ],
                                        className='text-center text-justify'
                                    ),
                                    dbc.ModalBody(
                                        children=[
                                            html.Div([
                                            dbc.Form([
                                            dbc.FormGroup([
                                                dbc.Label("En caso de requerirse, ¿Tiene la capacidad de trabajar desde casa?", style={'marginBottom': '25px'}),
                                                html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'Si', 'value': 'Si'},
                                                        {'label': 'Si pero no me convence', 'value': 'Si pero no me convence'},
                                                        {'label': 'No tengo la capacidad', 'value': 'No tengo la capacidad'},
                                                        {'label': 'No lo necesito, el negocio no lo requiere', 'value': 'No lo necesito, el negocio no lo requiere'},
                                                    ], id ="q1"
                                                    ),
                                                        ]),
                                                html.Br(),
                                            dbc.FormGroup([
                                                dbc.Label("¿Ha observado aumentos en los costos de su operación?", style={'marginBottom': '25px'}),
                                                html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'Si', 'value': 'Si'},
                                                        {'label': 'No', 'value': 'No'}
                                                    ], id="q2"
                                                    ),
                                                ]),
                                                html.Br(),
                                            dbc.FormGroup([
                                                dbc.Label("¿Cuál considera que sería la principal razón para cerrar su establecimiento?", style={'marginBottom': '25px'}),
                                                html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'Falta de fondos', 'value': 'Falta de fondos'},
                                                        {'label': 'Aumento de gastos', 'value': 'Aumento de gastos'},
                                                        {'label': 'Problemas de cobranza', 'value': 'Problemas de cobranza'},
                                                        {'label': 'Factores externos', 'value': 'Factores externos'},
                                                        {'label': 'Incertidumbre sobre las ventas', 'value': 'Incertidumbre sobre las ventas'},
                                                        {'label': 'Otro', 'value': 'Otro'}
                                                    ], id="q3"
                                                    ),
                                                ]),
                                                html.Br(),
                                            dbc.FormGroup([
                                                dbc.Label("¿Su establecimiento tiene la capacidad de pagar salarios si se mantiene cerrada o con trabajo desde casa?", style={'marginBottom': '25px'}),
                                                html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'Si, máximo 1 mes', 'value': '1'},
                                                        {'label': 'Si, máximo 2 meses', 'value': '2'},
                                                        {'label': 'Si, máximo 3 meses', 'value': '3'},
                                                        {'label': 'Si, más de 3 mes', 'value': '4'},
                                                        {'label': 'No', 'value': 'No'}
                                                    ], id="q4"
                                                    ),
                                                ]),
                                                html.Br(),
                                                dbc.FormGroup([
                                                    dbc.Label("¿Tomaría algún tipo de crédito para tener mayor liquidez?",
                                                              style={'marginBottom': '25px'}),
                                                    html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'Si', 'value': 'Si'},
                                                        {'label': 'No', 'value': 'No'}
                                                    ], id="q5"
                                                    ),
                                                ]),
                                                dbc.FormGroup([
                                                    dbc.Label(
                                                        "¿Ha tenido que subir precios para compensar mayores costos?",
                                                        style={'marginBottom': '25px'}),
                                                    html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'Si', 'value': 'Si'},
                                                        {'label': 'No', 'value': 'No'}
                                                    ], id="q6"
                                                    ),
                                                ]),
                                                dbc.FormGroup([
                                                    dbc.Label(
                                                        "¿Su establecimiento se ha visto en la necesidad de despedir personal?",
                                                        style={'marginBottom': '25px'}),
                                                    html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'No', 'value': 'No'},
                                                        {'label': 'Si', 'value': 'Si'},
                                                        {'label': 'No cuenta con personal', 'value': 'No cuenta con personal'},
                                                        {'label': 'No, pero lo esta considerando', 'value': 'No, pero lo esta considerando'},
                                                        {'label': 'No, pero se hará en los proximos días', 'value': 'No, pero se hará en los proximos días'}
                                                    ], id="q7"
                                                    ),
                                                ]),
                                                dbc.FormGroup([
                                                    dbc.Label(
                                                        "¿En qué porcentaje aproximadamente vio reducidas sus ventas?",
                                                        style={'marginBottom': '25px'}),
                                                    html.Br(),
                                                    dcc.Dropdown(options=[
                                                        {'label': 'No se tienen pérdidas', 'value': 'No se tienen pérdidas'},
                                                        {'label': 'Menos del 25%', 'value': 'Menos del 25%'},
                                                        {'label': 'Entre 25% y 50%',
                                                         'value': 'Entre 25% y 50%'},
                                                        {'label': 'Entre 50% y 75%',
                                                         'value': 'Entre 50% y 75%'},
                                                        {'label': 'Mas de 75%',
                                                         'value': 'Mas de 75%'}
                                                    ], id="q8"
                                                    ),
                                                ]),
                                                html.Br(),
                                                html.Div([
                                                html.Div(

                                                ),
                                                html.Div(
                                                dbc.Label(id="success", style={"color": "green", "marginTop": "15px"})
                                                )
                                                ], className='text-center text-justify')
                                            ], prevent_default_on_submit= True
                                            )
                                        ])

                                            ]

                                    ),
                                    dbc.ModalFooter(
                                        html.Div([
                                       dbc.Button([
                                           'Enviar'],
                                            id={"index": 1, "role": "close"},
                                            color="primary",
                                            className='ml-auto'

                                       )], className="text-center")
                                    ),
                                ],
                                id={"index": 1, "role": "modal"},
                                centered = True,
                                autoFocus = True,
                                scrollable=True,
                                size="lg"

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
    Output({'index': MATCH, 'role': 'modal'}, "is_open"),
    [Input({'index': MATCH, 'role': 'open'}, "n_clicks"),
     Input({'index': MATCH, 'role': 'close'}, "n_clicks")],
    [State({'index': MATCH, 'role': 'modal'}, "is_open")],
)
def toggle_modal_form(n1, n2, is_open):
    if n1 or n2 :
        return not is_open
    return is_open


@app.callback(
    Output({'index': MATCH, 'role': 'close'}, "disabled"),
    [
    Input("q1", "value"),
    Input("q2", "value"),
    Input("q3", "value"),
    Input("q4", "value"),
    Input("q5", "value"),
    Input("q6", "value"),
    Input("q7", "value"),
    Input("q8", "value")
    ]
)
def block_button(q1, q2, q3, q4, q5, q6, q7, q8):
    if q1 == None or q2 == None or q3 == None or q4 == None or q5 == None or q6 == None or q7 == None or q8 == None:
        return True
    else:
        return False
