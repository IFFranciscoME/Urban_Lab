# .. ................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos        .. #
# .. Archivo: visualizaciones.py - diccionario con datos de entrada                      .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                  .. #
# .. Licencia: Todos los derechos reservados                                             .. #
# .. Repositorio: https://github.com/IFFranciscoME/Urban_Lab.git                         .. #
# .. ................................................................................... .. #


# Importar librerias
import plotly.express as px
import plotly.graph_objects as go
import geojson
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
from config.config import db


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Histograma de metrica estres y adaptabilidad
# -- ------------------------------------------------------------------------------------ -- #
def histogram_metric(p_data, p_metric):
    """
    Histograma y estadistidicas descriptivas

    Parameters
    ---------
    p_data: DataFrame : datos de pymes con columna de metrica
    p_metric: str : nombre de la metrica

    Returns
    ---------
    fig : plotly figure : mapa de la zmg de jalisco

    Debuggin
    ---------
    p_df_data = metric_quantification(df_pymes, ent.conditions_stress,
                                   'Estres')['df_prices']
    p_metric = 'Estres'

    """
    data = p_data['Total']
    fig = make_subplots(rows=2, cols=1,
                        specs=[[{"type": "xy"}], [{"type": "domain"}]],
                        subplot_titles=(
                                "Histograma",
                                "Datos estadísticos"),
                       vertical_spacing=0.3)

    color = 'rgb(230, 120, 100)' if p_metric=='Estres' else 'rgb(200, 120, 200)'
    titulo = 'Estrés' if p_metric == 'Estres' else 'Adaptabilidad'

    # Histograma
    fig.add_trace(go.Histogram(x=data,
                               opacity=0.7,
                               marker=dict(color=color)
                               ),
                  row=1, col=1)

    # Tabla descriptiva de datos
    t_descriptive = data.describe().round(2)

    # Colores de head and body de tabla de acuerdo a metrica
    color_h = 'rgb(160, 85, 70)' if p_metric=='Estres' else 'rgb(130, 20, 100)'
    color_b = 'rgb(230, 190, 180)' if p_metric=='Estres' else 'rgb(220, 180, 200)'

    fig.add_trace(go.Table(name='Descripcion',
                header=dict(values=[' ', titulo],
                            fill_color=color_h,
                            align='center',
                            font_color='White',
                            font_size=14
                            ),
                cells=dict(values=[t_descriptive.index.tolist(), t_descriptive],
                           fill_color =color_b)
                           ),
                  row=2, col=1)

    # Axis title
    fig['layout']['xaxis']['title']='Nivel de '+ titulo
    fig['layout']['yaxis']['title']='Frecuencia'
    
    fig.update_layout(
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )
    return fig


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Mapa
# -- ------------------------------------------------------------------------------------ -- #
def map_metric(p_df_data, p_metric, color):
    """
    Visualizacion de mapa por metrica

    Parameters
    ---------
    p_df_data: DataFrame : datos de pymes con columna de metrica
    metric: str : nombre de la metrica
    color: str : colores para metrica

    Returns
    ---------
    fig : plotly figure : mapa de la zmg de jalisco

    Debuggin
    ---------
    p_df_data = metric_quantification(df_pymes, ent.conditions_stress,
                                   'Estres')['df_prices']
    metric = 'Estres'
    color = "Reds"

    """
    with open(db + 'CP_2.json') as f:
        j_file = geojson.load(f)
    fig = px.choropleth_mapbox(
        p_df_data,
        geojson=j_file,
        locations='CP',
        color=p_metric,
        color_continuous_scale=color,
        range_color=(
            min(p_df_data[p_metric]),
            max(p_df_data[p_metric])
        ),
        mapbox_style="carto-positron",
        zoom=10,
        center={
            "lat": 20.666820,
            "lon": -103.3918228
        },
        opacity=0.5,
        labels={
            p_metric: 'Nivel de ' + p_metric
        }
    )
    # titulos
    titulo = 'Estrés' if p_metric == 'Estres' else 'Adaptabilidad'

    fig.update_layout(
        title_text=titulo+ ' de la ZMG por código postal',
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )

    return fig


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Velocimetro por tamaño de pyme
# -- ------------------------------------------------------------------------------------ -- #
def velocimeter_size(p_df_data, p_metric, p_metric_table):
    """
    Parameters
    ---------
    p_df_data: DataFrame : datos de pymes en dataframe
    p_metric: str : nombre de la metrica
    p_metric_table: DataFrame : matriz del calculo de la metrica

    Returns
    ---------
    fig : plotly figure : mapa de la zmg de jalisco

    Debuggin
    ---------
    p_df_data = df_pymes
    p_metric = 'Estres'
    p_metric_table = pr.metric_quantification(df_pymes,
                                       ent.conditions_stress, 'Estres')['metric_table']

    """
    # Hacer copia
    metric_table = p_metric_table.copy()
    # Añadir columna necesaria
    metric_table['Tamaño'] = p_df_data['Tamaño']
    # Creación de tabla resumen
    pivot_size = pd.pivot_table(
        metric_table,
        index=['Tamaño'],
        values=list(metric_table.columns),
        aggfunc=np.median
    )
    # Creacion de figura
    fig = go.Figure()

    # limites
    lim = metric_table['Total'].max()
    # color
    color = "darkred" if p_metric == 'Estres' else "mediumpurple"
    fig.add_trace(go.Indicator(
        value=pivot_size.loc['Micro', 'Total'],
        title={'text': "Micro"},
        gauge={
            'bar': {'color': color},
            'axis': {
                'range': [None, lim],
                'visible': False
            }
        },
        domain={'row': 0, 'column': 0}
    ))

    fig.add_trace(go.Indicator(
        value=pivot_size.loc['Pequeña', 'Total'],
        title={'text': "Pequeña"},
        gauge={
            'bar': {'color': color},
            'axis': {'range': [None, lim], 'visible': False}
        },
        domain={'row': 0, 'column': 1}
    ))

    fig.add_trace(go.Indicator(
        value=pivot_size.loc['Mediana', 'Total'],
        title={'text': "Mediana"},
        gauge={
            'bar': {
                'color': color
            },
            'axis': {
                'range': [None, lim],
                'visible': False
            }
        },
        domain={'row': 1, 'column': 0}
    ))

    fig.add_trace(go.Indicator(
        value=pivot_size.loc['Grande', 'Total'],
        title={'text': "Grande"},
        gauge={
            'bar': {
                'color': color
            },
            'axis': {
                'range': [None, lim],
                'visible': False}
        },
        domain={
            'row': 1,
            'column': 1
        }
    ))

    titulo = 'Estrés' if p_metric == 'Estres' else 'Adaptabilidad'

    fig.update_layout(
        title=titulo + " medio de los tamaños de empresas",
        grid={'rows': 2, 'columns': 2, 'pattern': "independent"},
        template={
            'data': {
                'indicator': [
                    {
                        'title': {'text': "Tamaño"},
                        'mode': "number+gauge"
                    }
                ]
            }
        },
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )

    return fig


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: De barras por municipio
# -- ------------------------------------------------------------------------------------ -- #
def bars_city(p_df_data, p_metric, p_metric_table):
    """
    Parameters
    ---------
    p_df_data: DataFrame : datos de pymes en dataframe
    p_metric: str : nombre de la metrica
    p_metric_table: DataFrame : matriz del calculo de la metrica

    Returns
    ---------
    fig : plotly figure : mapa de la zmg de jalisco

    Debuggin
    ---------
    p_df_data = df_pymes
    p_metric = 'Estres'
    p_metric_table = pr.metric_quantification(df_pymes,
                                       ent.conditions_stress, 'Estres')['metric_table']

    """
    # Hacer copia
    metric_table = p_metric_table.copy()
    # Añadir columna necesaria
    metric_table['Municipio'] = p_df_data['Municipio']
    # Creación de tabla resumen
    pivot_mun = pd.pivot_table(
        metric_table,
        index=['Municipio'],
        values=list(metric_table.columns),
        aggfunc=np.median
    )
    # Creacion de figura
    fig = go.Figure()
    # Colores
    colors = px.colors.sequential.Reds[3:9] if p_metric == 'Estres' else px.colors.sequential.Purp[1:7]
    # limites
    lim = metric_table['Total'].max()
    # figura
    fig = go.Figure(
        data=[go.Bar(
            x=pivot_mun.index,
            y=pivot_mun['Total'].sort_values(),
            marker_color=colors
        )],
        layout={
            'yaxis': {
                'range': [0, lim]
            }
        }
    )
    # Tilde en estres
    titulo = 'Estrés' if p_metric == 'Estres' else 'Adaptabilidad'

    fig.update_layout(
        title=titulo + " medio por Municipio de la ZMG",
        xaxis_title="Municipios",
        yaxis_title=p_metric,
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        hovermode='closest'
    )

    return fig


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Tabla de giro
# -- ------------------------------------------------------------------------------------ -- #
def table_giro(p_df_data, p_metric, p_metric_table):
    """
    Parameters
    ---------
    p_df_data: DataFrame : datos de pymes en dataframe
    p_metric: str : nombre de la metrica
    p_metric_table: DataFrame : matriz del calculo de la metrica

    Returns
    ---------
    fig : plotly figure : mapa de la zmg de jalisco

    Debuggin
    ---------
    p_df_data = df_pymes
    p_metric = 'Estres'
    p_metric_table = pr.metric_quantification(df_pymes,
                                       ent.conditions_stress, 'Estres')['metric_table']


    """
    # Agregar columna de giro
    p_metric_table['Giro'] = p_df_data['Giro']
    # Creación de tabla resumen
    pivot_giro = pd.pivot_table(
        p_metric_table,
        index=['Giro'],
        values=list(p_metric_table.columns),
        aggfunc=np.median
    ).round(3)
    # Cambiar nombre de columnas
    def change_name_columns(x): return x.replace('_', ' ').title()
    # Nuevas columnas
    new_col = list(map(change_name_columns, list(pivot_giro.columns)))[1:]

    # En vez de total, nombre de metrica
    new_col.insert(0, p_metric)

    # Renombrar columnas de la pivot de giro
    pivot_giro.columns = new_col

    # Columnas de giro
    column_giro = list(pivot_giro.columns)

    # Tomar lista de columnas de la pivote
    list_col = [pivot_giro[c] for c in column_giro]

    # Agregar el indice
    list_col.insert(0, list(pivot_giro.index))

    # Colores
    color_h = 'rgb(160, 85, 70)' if p_metric == 'Estres' else 'rgb(80, 10, 90)'
    color_b = 'rgb(230, 190, 180)' if p_metric == 'Estres' else 'rgb(220, 180, 200)'

    # Titulo con tilde
    titulo = 'Estrés' if p_metric == 'Estres' else 'Adaptabilidad'

    fig = go.Figure(data=[
        go.Table(
            name=p_metric,
            header=dict(
                values=["Giro"] + pivot_giro.columns.tolist(),
                fill_color=color_h,
                align='center',
                font_color='White',
                font_size=11
            ),
            cells=dict(
                values=list_col,
                fill_color=color_b,
                align='center',
                height=40,
                font_size=11
            )
        )
    ])

    fig.update_layout(
        title="Datos para el cálculo de la métrica: "+titulo,
        margin={"r": 10, "t": 40, "l": 10, "b": 10},
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )

    return fig


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: tabla de precios
# -- ------------------------------------------------------------------------------------ -- #
def table_prices(p_df_semaforo):
    """
    Visualizacion de la tabla en plotly del semaforo de precios que se calcula con
    la funcion de semaforo que se encuentra en proceso

    Parameters
    ---------
    p_df_semaforo: DataFrame : datos del semaforo en un DataFrame

    Returns
    ---------
    fig : plotly figure : tabla de semforo de precios

    Debuggin
    ---------
    p_df_semaforo = proceso.semaforo_precios(df_prices)['semaforo']


    """
    # resultados
    values = list(p_df_semaforo[0])
    # colores verde | amarillo | rojo
    colores = [
        'rgb(200, 230, 150)',
        'rgb(245, 220, 130)',
        'rgb(230, 120, 100)'
    ]
    # asignar colores
    def asig_colors(x): return colores[2] if x == 'rojo' else (
        colores[0] if x == 'verde' else colores[1])
    # colores de tabla
    colors_t = list(map(asig_colors, values))

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[
                '<b>Productos - grupo</b>',
                '<b>Resultado de predicción %</b>'
            ],
            line_color='white',
            fill_color='rgb(240, 225, 230)',
            align='center',
            font=dict(
                color='rgb(110, 90, 100)',
                size=18
            )
        ),
        cells=dict(
            values=[list(p_df_semaforo.index), list(p_df_semaforo[1])],
            line_color=['rgb(235, 225, 245)', 'white'],
            fill_color=['white', colors_t],
            align='center'
        ))
    ])

    fig.update_layout(
        height=465,
        title="Predicciones de la variación de precios (Mayo a Noviembre 2020)",
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        title_x=0.5,
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )

    return fig


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: diferencias de los precios
# -- ------------------------------------------------------------------------------------ -- #
def dif_prices(p_df_predicciones, p_grupo):
    """
    Visualizacion de las diferencias de la mediana del ultimo precio por clase
    con respecto a la prediccion

    Parameters
    ---------
    p_df_predicciones: DataFrame : resultado de predicciones
    p_grupo: str : nombre del grupo de productos

    Returns
    ---------
    fig : plotly figure : mapa de la zmg de jalisco

    Debuggin
    ---------
    p_df_predicciones = proceso.semaforo_precios(df_prices)['predicciones']
    p_grupo = 'Alimentos'

    """
    # Transponer
    predicciones = p_df_predicciones.T
    # Tomar datos del grupo
    grupo = predicciones[p_grupo]

    # Margenes de acuerdo al tamaño
    marg = {'t': 200, 'b': 200, 'l': 250, 'r': 20} if len(grupo.T) == 1 else (
        {'t': 100, 'b': 100, 'l': 250, 'r': 20} if len(grupo.T) == 4 else (
            {'t': 150, 'b': 150, 'l': 250, 'r': 20}))
    # Espacio vertical
    v_s = 0.2 if len(grupo.T) == 4 else 0.45

    # colores: rojo | amarillo | verde
    colores = ['rgb(230, 120, 100)', 'rgb(245, 220, 130)', 'rgb(200, 230, 150)']

    if len(grupo.T) == 8:
        # Tipo de fig que se añadiran al subplot
        tipos = [[{"type": "indicator"}, {"type": "indicator"}]
                 for i in range(4)]
        fig = make_subplots(rows=4, cols=2, specs=tipos,
                            vertical_spacing=0.2, horizontal_spacing=0.3)
        rows = [1, 2, 3, 4, 1, 2, 3, 4]
        cols = [1, 1, 1, 1, 2, 2, 2, 2]

        # Para las 8
        for i in range(len(grupo.T)):
            # Datos que se necesitan de cada clase del grupo
            titulo = list(grupo.columns)[i]
            ultimo_precio = grupo.iloc[0, i]
            futuro_precio = grupo.iloc[1, i]

            # Color de barra
            color = colores[0] if futuro_precio > ultimo_precio else (
                            colores[2] if ultimo_precio > futuro_precio else colores[1])

            # Añadir fig
            fig.append_trace(go.Indicator(
                mode="number+gauge", value=futuro_precio,
                delta={'reference': ultimo_precio},
                title={'text': titulo, 'font': {'size': 9}},
                gauge={
                    'shape': "bullet",
                    'axis': {
                        'range': [ultimo_precio * .85, futuro_precio * 1.1]
                    },
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': ultimo_precio},
                    'steps': [{
                        'range': [ultimo_precio * .85, ultimo_precio],
                        'color': "white"
                    }],
                    'bar': {'color': color}
                }
            ), row=rows[i], col=cols[i])
        # Layout de fig
        fig.update_layout(
            title="Precios para Nov 2020 con respecto al precio de Mayo 2020 de:" + p_grupo,
            title_x=0.5,
            titlefont=dict(size=15),
            height=450,
            margin={'t': 100, 'b': 100, 'l': 150, 'r': 10},
            font={
                'color': "black",
                'family': "Arial",
                'size': 14
            },
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9"
        )

    else:
        # Los tipos de graficas
        tipos = [[{"type": "indicator"}] for i in range(len(grupo.T))]

        # Hacer subplots
        fig = make_subplots(rows=len(grupo.T), cols=1,
                            specs=tipos, vertical_spacing=v_s)

        for i in range(len(grupo.T)):
            # Datos que se necesitan de cada clase del grupo
            titulo = list(grupo.columns)[i]
            ultimo_precio = grupo.iloc[0, i]
            futuro_precio = grupo.iloc[1, i]

            # Color de barra
            color = colores[0] if futuro_precio > ultimo_precio else (
                colores[2] if ultimo_precio > futuro_precio else colores[1])

            # Añadir plots
            fig.append_trace(go.Indicator(
                mode="number+gauge",
                value=futuro_precio,
                delta={
                    'reference': ultimo_precio
                },
                domain={
                    'x': [0.25, 1],
                    'y': [0.7, 0.9]
                },
                title={
                    'text': titulo,
                    'font': {'size': 11}
                },
                gauge={
                    'shape': "bullet",
                    'axis': {
                        'range': [ultimo_precio * .85, futuro_precio * 1.1]
                    },
                    'threshold': {
                        'line': {
                            'color': "black",
                            'width': 2
                        },
                        'thickness': 0.75,
                        'value': ultimo_precio
                    },
                    'steps': [{
                        'range': [ultimo_precio * .85, ultimo_precio],
                        'color': "white"
                    }],
                    'bar': {
                        'color': color
                    }
                }), row=i + 1, col=1)

        # Layout general
        fig.update_layout(
            title="Precios para Nov 2020 con respecto al precio de Mayo 2020 de: " + p_grupo,
            title_x=0.5,
            titlefont=dict(size=15),
            height=450,
            margin=marg,
            font={'color': "black", 'family': "Arial", 'size': 14},
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9"
        )

    return fig


def add_porcentual(p_df_predicciones):
    """
    Función que hace el cálculo del cambio porcentual en precios y
	que adecua el df para la realización de las tablas.

    Parameters
    ---------
    p_df: DataFrame : df que contiene el último precio y
						el precio estimado a 6 meses por grupos y clases.

    Returns
    ---------
    df:  DataFrame : df que contiene lo que el anterior y
						el cambio porcentual de los precios.

    Debuggin
    ---------
    p_df = add_procentual(df)

    """
    # Copia de Dataframe de predicciones
    p_df = p_df_predicciones.copy()

    # Agregar columna de cambio porcentual
    p_df['C_Porcentual'] = round((
        p_df['Precio para Nov 2020'] / p_df['Ultimo precio'] - 1)*100, 4)

    # Reiniciar indices, sin multi-index
    p_df.reset_index(level=1, inplace=True)
    p_df.reset_index(level=0, inplace=True)

    # Renombrar columnas
    p_df = p_df.rename(columns={'index': 'Grupo', 'level_1': 'Clase'})

    # Calcular para colorear
    color = ['Precios que bajaran más de 1%' if p_df['C_Porcentual'][i] <= -1 else (
        'Precios que se mantendrán con una variación menor a 1%' if p_df[
            'C_Porcentual'][i] <= 1 and p_df[
                'C_Porcentual'][i] > -1 else 'Precios que aumentarán más de 1%'
    ) for i in range(len(p_df))]

    # Añadir columna de colores
    p_df['Color'] = color

    return p_df


def treemap_chart(p_df, path, color=[]):
    """
    Función que crea la tabla treemap

    Parameters
    ---------
    p_df: DataFrame : df que contiene los precios, su cambio y el color asignado.
    path: list : lista que contiene los labels a mostrar en la tabla.
    color: list : lista que contiene los colores a mostrar.

    Returns
    ---------
    fig: chart: Tabla que se solicita.

    Debuggin
    ---------
    path = ['Grupo','Clase', 'C_Porcentual']
    color = ["yellow", "red", "green"]
    p_df = treemap_chart(p_df, path, color)

    """
    # Crear pigura de treemap
    fig = px.treemap(p_df, path=path)
    # Poner color
    fig.update_layout(treemapcolorway=color)
    # Etiquetas
    fig.update_traces(hovertemplate='<b>%{label}')
    # Titulo
    fig.update_layout(
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        title_text='Cambios Porcentuales en los precios por Grupo',
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )

    return fig


def treemap_prices(p_df_predicciones):
    """
    Función que crea la tabla treemap

    Parameters
    ---------
    p_df: DataFrame : df que contiene los precios, su cambio y el color asignado.

    Returns
    ---------
    fig: chart: Tabla que se solicita.

    Debuggin
    ---------
    path = df_predicciones
    """
    # Añadir columna de cambio porcentual y quitar multi-index
    df_porc = add_porcentual(p_df_predicciones)
    # Columnas
    path = ['Color', 'Grupo', 'Clase', 'C_Porcentual']
    # Colores amarillo | rojo | verde
    color = ['rgb(245, 220, 130)', 'rgb(230, 120, 100)', 'rgb(200, 230, 150)']
    # label = df_porc['Clase']
    df_porc['C_Porcentual'] = df_porc['C_Porcentual'].apply(
        lambda x: ' Cambio Porcentual: ' + str(x))
    # Generar figura
    fig = treemap_chart(df_porc, path, color)
    fig.update_layout(
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )
    return fig


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: info precios
# -- ------------------------------------------------------------------------------------ -- #
def table_prices_data(p_df_prices):
    """
    Función que crea la tabla de datos

    Parameters
    ---------
    p_df: DataFrame : df que contiene los precios

    Returns
    ---------
    fig: chart: Tabla que se solicita.

    Debuggin
    ---------
    path = df_prices

    """
    # Tomar sólo columnas que se necesitan mostrar
    df = p_df_prices.iloc[:, 1:4].merge(
        p_df_prices.iloc[:, -5:], left_index=True, right_index=True)

    # Sacar la mediana por producto generico
    df_med = df.groupby('Generico').median().reset_index().round(2)

    # Lista del groupby
    list_groups = list(df.groupby('Generico'))

    # Tomar las columnas de grupo y clase que hacen falta en el df de mediana
    grup_clas = pd.DataFrame(
        [list_groups[i][1].iloc[0, 0:2].T for i in range(len(list_groups))])
    # Reiniciar indice para hacer merge
    grup_clas.reset_index(drop=True, inplace=True)

    # Combinar los que se tienen de medianas con las columnas faltantes
    df_med_complet = grup_clas.merge(df_med, left_index=True, right_index=True)

    # Dataframe final acomodados por grupo
    df_final = df_med_complet.sort_values(by=['Grupo'])
    df_final.reset_index(drop=True, inplace=True)

    # Nombres de header de tabla
    col = df_final.columns.tolist()
    # Valores en losta del df
    val = [df_final[c] for c in col]

    # Table
    fig = go.Figure(data=[go.Table(name='Precios',
                                   header=dict(values=col,
                                               fill_color='rgb(95, 95, 80)',
                                               align='center', font_color='White', font_size=10),
                                   cells=dict(values=val,
                                              fill_color='rgb(250, 245, 200)',
                                              align='center', height=40, font_size=11))])

    fig.update_layout(
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        title_text='Datos de precios históricos',
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )
    return fig

# -- ------------------------------------------------------------------------------------ -- #
# -- Function: treemap de estres y adaptabilidad
# -- ------------------------------------------------------------------------------------ -- #
def treemap_giro(p_df_data, p_metric, p_metric_table):
    """
    Parameters
    ---------
    p_df_data: DataFrame : datos de pymes en dataframe
    p_metric: str : nombre de la metrica
    p_metric_table: DataFrame : matriz del calculo de la metrica

    Returns
    ---------
    fig : plotly figure : mapa de la zmg de jalisco

    Debuggin
    ---------
    p_df_data = df_pymes
    p_metric = 'Estres'
    p_metric_table = pr.metric_quantification(df_pymes,
                                       ent.conditions_stress, 'Estres')['metric_table']


    """
    # Cambiar nombre de columnas
    def change_name_columns(x): return x.replace('_', ' ').title()

    # Agregar columna de giro
    p_metric_table['Sector'] = p_df_data['Sector']

    # Creación de tabla resumen 1 - sector
    pivot_sec = pd.pivot_table(p_metric_table, index=['Sector'],
                               values=list(p_metric_table.columns), aggfunc=np.median)

    # Nuevas columnas
    new_col_sec = list(map(change_name_columns, list(pivot_sec.columns)))[1:]

    # En vez de total, nombre de metrica
    new_col_sec.insert(0, p_metric)

    # Renombrar columnas de la pivot de sector
    pivot_sec.columns = new_col_sec

    # ---------------------------------------------------------------

    # Agregar Giro
    p_metric_table['Giro'] = p_df_data['Giro']

    # Creación de tabla resumen 2 - sector y giro
    pivot_sector_giro = pd.pivot_table(p_metric_table, index=['Sector', 'Giro'],
                                       values=list(p_metric_table.columns), aggfunc=np.median)

    # Nuevas columnas
    new_col_sg = list(
        map(change_name_columns, list(pivot_sector_giro.columns)))[1:]

    # En vez de total, nombre de metrica
    new_col_sg.insert(0, p_metric)

    # Renombrar columnas de la pivot de giro
    pivot_sector_giro.columns = new_col_sg

    # Reset index y cambios de nombre a una columna
    pivot_sector_giro = pivot_sector_giro.reset_index()
    pivot_sec = pivot_sec.reset_index()

    pivot_sec = pivot_sec.rename(columns={'Sector': 'Giro'})

    # Crear DF concatenado
    concatenado = pd.concat([pivot_sec.loc[pivot_sec['Giro'] == "Comercio"],
                             pivot_sector_giro.loc[pivot_sector_giro['Sector']
                                                   == 'Comercio'],
                             pivot_sec.loc[pivot_sec['Giro']
                                           == "Construcción"],
                             pivot_sector_giro.loc[pivot_sector_giro['Sector']
                                                   == 'Construcción'],
                             pivot_sec.loc[pivot_sec['Giro'] == "Manufactura"],
                             pivot_sector_giro.loc[pivot_sector_giro['Sector']
                                                   == 'Manufactura'],
                             pivot_sec.loc[pivot_sec['Giro'] == "Servicios"],
                             pivot_sector_giro.loc[pivot_sector_giro['Sector']
                                                   == 'Servicios'],
                             ], ignore_index=False, sort=False)

    # Colores
    color = 'Reds' if p_metric == 'Estres' else 'Purples'

    # Creacion de figura
    values = concatenado[p_metric]
    labels = concatenado.Giro
    parents = concatenado.Sector

    fig = go.Figure(go.Treemap(
        labels=labels,
        values=values,
        parents=parents,
        marker_colorscale=color,
        textinfo="label+value"))

    titulo = 'Estrés' if p_metric == 'Estres' else 'Adaptabilidad'

    fig.update_layout(
        title="Datos por mediana para la métrica de: " + titulo + " (por sector)",
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )
    return fig
