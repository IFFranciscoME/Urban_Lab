import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
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
button_desc=dbc.Button("Descripción", id="open", style={"width": "150px", 'background': '#317CF6'})


modal1 = dbc.Modal([
    dbc.ModalHeader("Descripción"),
    dbc.ModalBody("Esta gráfica muestra el porcentaje de reducción de ventas contra la cantidad de empresas que han reportado dicha disminución. En el eje vertical representa la cantidad de empresas y el eje horizontal el porcentaje que han visto reducido en ventas."),
    dbc.ModalFooter(dbc.Button("Cerrar", id="close", color="secondary")),
], id="modal")


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
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal1(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



