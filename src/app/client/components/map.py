import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app.dash import app

from model.datos import dict_metrics_df, semaforo
from model.visualizaciones import map_metric, table_prices
from model.entradas import dict_colors

variables = {
    'Estres': {
        'variables-header': 'Estrés Económico',
        'variables-body': 'Se denomina estresor económico a todo estímulo externo que recibe una empresa y genera inestabilidad económica como por ejemplo: despidos, disminución en las ventas, etc. La variable estrés económico representa el estrés contraído por las empresas a partir de la suma de estos factores externos. Cada estímulo se midió con una frecuencia del 0 al 4 para poder categorizar de manera más sencilla para obtener un resultado más exacto.'
    },
    'Adaptabilidad': {
        'variables-header': 'Adaptabilidad',
        'variables-body': 'A raíz de la pandemia el ambiente físico ha sido alterado y manipulado, lo que ha generado nuevos patrones de actividad, por consiguiente la conducta de las empresas se ha visto modificada para poder responder de mejor o peor manera ante esta situación. A este tipo de acciones se las conoce como adaptabilidad, las cuales son habilidades sociales con las que cuentan los individuos para poder tener mayor funcionalidad, esto está representado en esta variable. Cada actividad  se midió con una frecuencia del 0 al 2 para poder categorizar de manera más sencilla para obtener un resultado más exacto.'
    },
    'Precios': {
        'variables-header': 'Predicción de Precios',
        'variables-body': 'Esta métrica se enfoca en la predicción de la variación de los precios de los insumos y algunos servicios en Guadalajara para los próximos 6 meses. Los insumos y servicios están organizados en 32 clases que a su vez forman parte de 14 grupos. Los colores que se presentan en la métrica tienen una dinámica de semáforo tomando como criterio el rojo siendo que los precios decrementen más de un 1%, el amarillo que no tengan un cambio muy significativo en el precio con una variación de -1% a 1% y el verde que tengan una variación al alza mayor a un 1%. Las grafica que se ve representada en pesos toma la mediana de los precios de los productos dentro de cada clase.'
    }
}

txt_variables = html.Div([
    html.H5(children=[], id='variables-header', className='text-center text-justify'),
    html.P(children=[], id='variables-body', className='text-justify')
],className='text-justify')

map_graph = dcc.Graph(id='map', figure={}, className='pb-3 pr-3 pl-3 mt-auto mb-auto')

# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        Output(
            component_id='variables-header',
            component_property='children'),
        Output(
            component_id='variables-body',
            component_property='children'
        ),
        Output(
            component_id='map',
            component_property='figure'
        )
    ],
    [Input(component_id='slct_map', component_property='value')]
)
def update_graph_bar(option_map):
    #container = 'La variable escogida por el usuario es: {}'.format(option_map)
    if option_map == 'Precios':
        fig = table_prices(semaforo)
    else:
        metric = dict_metrics_df[option_map]
        # Visualizations
        fig = map_metric(metric, option_map, dict_colors[option_map])

    header = variables[option_map]['variables-header']
    body = variables[option_map]['variables-body']

    return header, body, fig
