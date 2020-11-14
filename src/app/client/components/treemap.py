import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app.dash import app
from model.visualizaciones import table_giro, treemap_prices, treemap_giro, table_prices_data
from model.datos import dict_metrics_table, df_pymes, predicciones, df_prices

def treemapPrices():
    return treemap_prices(predicciones)

def tablePrices():
    return table_prices_data(df_prices)

def treemapGiro(option_map):
    return  treemap_giro(df_pymes, option_map,dict_metrics_table[option_map])

def tableGiro(option_map):
    return table_giro(df_pymes, option_map, dict_metrics_table[option_map])

figures= {
    'Precios':{
        'Treemap' :treemapPrices,
        'Datos': tablePrices
    },
    'NoPrecios' :{
        'Treemap' :treemapGiro,
        'Datos': tableGiro
    }
    
}

tabs_barchart = dcc.Tabs(id='tabs_data', value='Treemap', children=[
    dcc.Tab(label='Treemap', value='Treemap'),
    dcc.Tab(label='Datos', value='Datos'),
])

treemap = dcc.Graph(id='treemap', figure={}, className='')


@app.callback(
    Output(
        component_id='treemap',
        component_property='figure'
    ),
    [
        Input(
            component_id='slct_map',
            component_property='value'
        ),
        Input(
            component_id='tabs_data',
            component_property='value'
        )
    ]
)
def update_graph(option_map, option_data):
    # Visualizations
    if option_map == 'Filtros':
        return {}
    if option_map == 'Precios':
        fig = figures['Precios'][option_data]()
    else:
        fig = figures['NoPrecios'][option_data](option_map)

    return fig
#'slct_data'
