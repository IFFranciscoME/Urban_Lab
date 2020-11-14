import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app.dash import app
from model.filter_graphics import despidosGraphic, creditoGraphic, insumosGraphic, preciosGraphic, porcentajeGraphic, optionslct


def precios(sector, municipio, giro):
    return preciosGraphic(sector, municipio, giro)

def insumos(sector, municipio, giro):
    return  insumosGraphic(sector, municipio, giro)

def credito(sector, municipio, giro):
    return creditoGraphic(sector, municipio, giro)

def despidos(sector, municipio, giro):
    return despidosGraphic(sector, municipio, giro)



mapoptions1 = {
    '0': precios,
    '1': insumos
}

mapoptions2 = {
    '0': credito,
    '1': despidos
}

tabs_barchart1 = dcc.Tabs(id='tabs_fig1', value='0', children=[
    dcc.Tab(label='Aumento de precios', value='0'),
    dcc.Tab(label='Costo de insumos', value='1'),
])

tabs_barchart2 = dcc.Tabs(id='tabs_fig2', value='0', children=[
    dcc.Tab(label='Solicitud de credito', value='0'),
    dcc.Tab(label='Despido de personal', value='1'),
])

map_graphP1 = dcc.Graph(id='mapP1', figure={}, className='mt-auto mb-auto')
map_graphP2 = dcc.Graph(id='mapP2', figure={}, className='mt-auto mb-auto')
map_graphBars = dcc.Graph(id='mapBar', figure={}, className='mt-auto mb-auto')

modal_questions = dbc.Modal(
        [
        dbc.ModalHeader(
            children=[
                html.H1("Bienvenido a la herramienta de levantamiento de datos"),
                html.P("Apoyanos contestando las siguientes preguntas, con el fin de agregar información a nuestra bas de datos")
            ],
            className='text-center text-justify'
        ),
        dbc.ModalBody(
            children=[
                html.Form([
                    html.P(children=[
                        "Seleccione el sector en el que opera su empresa:",
                        dcc.Dropdown(options=[
                            {'label': 'Manufactura', 'value': 'Manufactura'},
                            {'label': 'Comercio', 'value': 'Comercio'},
                            {'label': 'Servicio', 'value': 'Servicio'},
                            {'label': 'Construcción', 'value': 'Construcción'},
                        ],
                            )
                    ]),
                    html.P(children=[
                        "¿Cuál ha sido el comportamiento de sus ventas del trimestre actual respecto al anterior?",
                        dcc.Dropdown(options=[
                            {'label': 'Se mantuvieron igual', 'value': 'Se mantuvieron igual'},
                            {'label': 'Se han reducido', 'value': 'Se han reducido'},
                            {'label': 'Se han aumentado', 'value': 'Se han aumentado'}
                        ],
                            )
                    ]),
                    html.P(children=[
                        "¿Cuál ha sido el comportamiento de sus  costos operativos?",
                        dcc.Dropdown(options=[
                            {'label': 'Se mantuvieron igual', 'value': 'Se mantuvieron igual'},
                            {'label': 'Se han reducido', 'value': 'Se han reducido'},
                            {'label': 'Se han aumentado', 'value': 'Se han aumentado'}
                        ],
                            )
                    ]),
                    html.P(children=[
                        "En el supuesto de no generar ventas en el futuro, ¿Cuántas semanas soportarían sus fondos para pagar todos sus gastos?",
                        dcc.RadioItems(options=[
                            {'label': '0 a 6 semanas', 'value': '1'},
                            {'label': '6 a 12 semanas', 'value': '1'},
                            {'label': '12 a 18 semanas', 'value': '2'},
                            {'label': '18 a 24 semanas o más', 'value': '2'}
                        ],
                            )
                    ]),
                    html.P(children=[
                        "Indique el porcentaje aproximado de aumento o reducción en ventas del trimestre actual respecto al anterior:",
                        dcc.Slider(min=0, max=100, step=1, value=100)
                    ])

                ])
                ],
            className='text-center text-justify'
        ),
        dbc.ModalFooter(
            dbc.Button([
                'Enviar',
                html.I(className='fas fa-times-circle')
            ],
                id='send-modal-questions',
                className='m-auto btn btn-success'
            )
        ),
    ],
    id = 'modal-questions',
    centered = True,
    autoFocus = True
)


@app.callback(
    [
    Output(
        component_id='mapP1',
        component_property='figure'
    ),
    Output(
        component_id='mapP2',
        component_property='figure'
    ),
    Output(
        component_id='mapBar',
        component_property='figure'
    ),
    Output(
        component_id='sectorSlct',
        component_property='disabled'
    ),
    Output(
        component_id='municipioSlct',
        component_property='disabled'
    ),
    Output(
        component_id='giroSlct',
        component_property='disabled'
    ),
    Output(
        component_id='municipioSlct',
        component_property='options'
    ),
    Output(
        component_id='giroSlct',
        component_property='options'
    )
    ],
    [
    Input(
        component_id='tabs_fig1',
        component_property='value'
     ),
    Input(
        component_id='tabs_fig2',
        component_property='value'
    ),

    Input(
        component_id='sectorSlct',
        component_property='value'
    ),
    Input(
        component_id='municipioSlct',
        component_property='value'
    ),
    Input(
        component_id='giroSlct',
        component_property='value'
    ),
    Input(
        component_id='sectorcheck',
        component_property='value'
    ),
    Input(
        component_id='girocheck',
        component_property='value'
    ),
    Input(
        component_id='municipiocheck',
        component_property='value'
    )
    ]
)
def setGraphsFilter(tabs1, tabs2, sector, municipio, giro, block_sec, block_giro, block_mun):
    global options_giro, options_municipio
    municipio_ops = optionslct('Municipio', sector)
    giro_ops = optionslct('Giro', sector)

    options_giro = [
                    {'label': name,
                    'value': name} for name in giro_ops
                  ]
    options_municipio = [
                     {'label': name,
                       'value': name} for name in municipio_ops
                  ]
    if block_sec == ['X']:
        sector = 'vacio'
        dis_sector='True'
        municipio_ops = optionslct('Municipio', None)
        giro_ops = optionslct('Giro', None)

        options_giro = [
            {'label': name,
             'value': name} for name in giro_ops
        ]
        options_municipio = [
            {'label': name,
             'value': name} for name in municipio_ops
        ]
    else:
        dis_sector = None

    if block_mun == ['X']:
        municipio = 'vacio'
        dis_municipio='True'
    else:
        dis_municipio = None

    if block_giro == ['X']:
        giro = 'vacio'
        dis_giro ='True'
    else:
        dis_giro=None






    map1 = mapoptions1[tabs1](sector, municipio, giro)
    map2 = mapoptions2[tabs2](sector, municipio, giro)
    bars = porcentajeGraphic(sector, municipio, giro)
    #print(map1)
    #print(map2)
    #print(bars)
    return map1, map2, bars, dis_sector, dis_municipio, dis_giro, options_municipio, options_giro


@app.callback(
    Output('modal-questions', 'is_open'),
    [
        Input('newdata', 'n_clicks'),
        Input('send-modal-questions', 'n_clicks')
    ],
    [State('modal-questions', 'is_open')],
)
def toggle_modal_barchart(n1, n2, is_open):
    if n1 or n2:
        return not is_open

    return is_open



