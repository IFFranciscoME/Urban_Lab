import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app.dash import app
from model.visualizaciones import bars_city, velocimeter_size, dif_prices, histogram_metric
from model.datos import dict_metrics_table, df_pymes, predicciones

groups = [
    'Alimentos',
    'Ropa',
    'Cuidado personal',
    'Salud',
    'Transporte público'
]

'''
txt_barchart = html.Div([
    html.H5(children=['']),
    html.P(children=[''])
],
id='txt_barchart',
className='d-none')
'''


def bars(option_map):
    return bars_city(df_pymes, option_map, dict_metrics_table[option_map])


def velocimeter(option_map):
    return velocimeter_size(df_pymes, option_map, dict_metrics_table[option_map])


def histogram(option_map):
    return histogram_metric(dict_metrics_table[option_map], option_map)


figures = {
    '0': bars,
    '1': velocimeter,
    '2': histogram
}

dropdown_barchart = dcc.Dropdown(
    id='slct_fig',
    options=[
        {'label': groups[0], 'value': 0},
        {'label': groups[1], 'value': 1},
        {'label': groups[2], 'value': 2},
        {'label': groups[3], 'value': 3},
        {'label': groups[4], 'value': 4}
    ],
    multi=False,
    clearable=False,
    value='1',
    className='d-none',
)

tabs_barchart = dcc.Tabs(id='tabs_fig', value='0', children=[
    dcc.Tab(label='Distribución por Municipio', value='0'),
    dcc.Tab(label='Tamaño de Empresas ZMG', value='1'),
    dcc.Tab(label='Histograma de Métrica', value='2'),
])

btn_barchart = dbc.Button([
    'Descripción ',
    html.I(className='fas fa-search-plus')
],
    id='open-modal-barchart',
    className='d-none'
)


output_barchart = html.Div([
    btn_barchart,
    dropdown_barchart,
    tabs_barchart
], className='mb-1')

barchart = dcc.Graph(
    id='barchart',
    figure={},
    className='mt-auto mb-auto'
)


modal_barchart = dbc.Modal(
    [
        dbc.ModalHeader(
            children=['Grafica de variación de precios en pesos'],
            className='text-center text-justify'
        ),
        dbc.ModalBody(
            children=['En esta grafica se observa una predicción en pesos de lo que variaran los precios dentro de 6 meses. El numero representado al final de la gráfica es una media de los precios futuros de todos los productos dentro de esa categoría. Por lo que es un precio representativo de lo que estarán los precios en un futuro. El numero en color verde o rojo representa cuantos pesos van a subir o bajar los productos. Ejemplo en los Alimentos en la clase de Carnes se ve el numero verde 1.42, lo que significa que en general los productos de carne estarán 1.42 pesos más caros en noviembre. La grafica representa una barra horizontal y una línea vertical, la línea vertical representa los precios actuales  y la barra horizontal representa los precios futuros.'],
            className='text-center text-justify'
        ),
        dbc.ModalFooter(
            dbc.Button([
                'Cerrar ',
                html.I(className='fas fa-times-circle')
            ],
                id='close-modal-barchart',
                className='m-auto btn btn-danger'
            )
        ),
    ],
    id='modal-barchart',
    centered=True,
    autoFocus=True
)

# Connect the Plotly graphs with Dash Components


@app.callback(
    Output(
        component_id='barchart',
        component_property='figure'
    ),
    [
        Input(
            component_id='slct_map',
            component_property='value'
        ),
        Input(
            component_id='slct_fig',
            component_property='value'
        ),
        Input(
            component_id='tabs_fig',
            component_property='value'
        )
    ]
)
def update_graph(option_map, figura_slct, figura_tabs):
    # Visualizations
    if option_map == 'Precios':
        fig = dif_prices(predicciones, groups[int(figura_slct)])
    else:
        fig = figures[figura_tabs](option_map)

    return fig

# Connect the Plotly graphs with Dash Components


@app.callback(
    [
        Output(
            component_id='open-modal-barchart',
            component_property='className'
        ),
        Output(
            component_id='slct_fig',
            component_property='className'
        ),
        Output(
            component_id='tabs_fig',
            component_property='className'
        )
    ],
    [Input(
        component_id='slct_map',
        component_property='value'
    )]
)
def update_graph(option_map):
    # Visualizations
    if option_map == 'Precios':
        return 'd-block btn btn-outline-primary bg-primary text-white float-left mr-auto', 'd-block float-right ml-auto w-25', 'd-none'

    return 'd-none', 'd-none', 'd-block'


@app.callback(
    Output('modal-barchart', 'is_open'),
    [
        Input('open-modal-barchart', 'n_clicks'),
        Input('close-modal-barchart', 'n_clicks')
    ],
    [State('modal-barchart', 'is_open')],
)
def toggle_modal_barchart(n1, n2, is_open):
    if n1 or n2:
        return not is_open

    return is_open
