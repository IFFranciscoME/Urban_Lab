# Importar librerias
import plotly.express as px
import plotly.graph_objects as go
import geojson
import pandas as pd
import numpy as np
import plotly.graph_objects as po
from collections import Counter

import dash_core_components as dcc

data_c = pd.read_excel('./src/db/data.xlsx', sheet_name = 'BD_Monitoreo')
df_c = data_c.filter(items = ['Sector', 'Municipio', 'Giro','ventas_porcentaje',
                         'despidos', 'credito', 'credito_solicitud', 'aumento_insumos',
                          'aumento_precios'])


def optionslct(data, sector): #data = 'Giro'
    if sector == None:
        df = df_c[data]
        return np.sort(pd.unique(df))
    else:
        df = []
        for i in range(len(df_c[data])):
            if df_c['Sector'][i]==sector:
                df.append(df_c[data][i])
        return np.sort(pd.unique(df))


def filterdf(user_input1, user_input2, user_input3):
    if user_input1 != 'vacio':
        if user_input2 != 'vacio':
            if user_input3 != 'vacio':
                df = df_c[(df_c['Sector'] == user_input1) & (df_c['Municipio'] == user_input2) & (
                            df_c['Giro'] == user_input3)].reset_index()
                return df
            else:
                df = df_c[(df_c['Sector'] == user_input1) & (df_c['Municipio'] == user_input2)].reset_index()
                return df
        elif user_input3 != 'vacio':
            df = df_c[(df_c['Sector'] == user_input1) & (df_c['Giro'] == user_input3)].reset_index()
            return df
        else:
            df = df_c[(df_c['Sector'] == user_input1)].reset_index()
            return df
    elif user_input2 != 'vacio':
        if user_input3 != 'vacio':
            df = df_c[(df_c['Municipio'] == user_input2) & (df_c['Giro'] == user_input3)].reset_index()
            return df
        else:
            df = df_c[(df_c['Municipio'] == user_input2)].reset_index()
            return df
    else:
        df = df_c[(df_c['Giro'] == user_input3)].reset_index()
        return df

def filterdata(user_input1, user_input2, user_input3):
    if user_input1 != 'vacio':
        if user_input2 != 'vacio':
            if user_input3 != 'vacio':
                data = data_c[(data_c['Sector'] == user_input1) & (data_c['Municipio'] == user_input2) & (
                            data_c['Giro'] == user_input3)].reset_index()
                return data
            else:
                data = data_c[(df_c['Sector'] == user_input1) & (data_c['Municipio'] == user_input2)].reset_index()
                return data
        elif user_input3 != 'vacio':
            data = data_c[(data_c['Sector'] == user_input1) & (data_c['Giro'] == user_input3)].reset_index()
            return data
        else:
            data = data_c[(data_c['Sector'] == user_input1)].reset_index()
            return data
    elif user_input2 != 'vacio':
        if user_input3 != 'vacio':
            data = data_c[(data_c['Municipio'] == user_input2) & (data_c['Giro'] == user_input3)].reset_index()
            return data
        else:
            data = data_c[(data_c['Municipio'] == user_input2)].reset_index()
            return data
    else:
        data = data_c[(data_c['Giro'] == user_input3)].reset_index()
        return data




#despidos
def despidosGraphic(sector, municipio, giro):
    df = filterdf(sector, municipio, giro) # codigo que filtra --- este es para las graficas
    data = filterdata(sector, municipio, giro)# codigo que filtra ---- este es para las metricas
    if df.empty:
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No existe información con los filtros seleccionados",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }
    si=0 
    no = 0 
    np = 0 
    nc=0 
    npd=0

    for i in range(0, len(data)):
        if df['despidos'][i] == 'No':
            no += 1
        if df['despidos'][i] == 'No cuenta con personal':
            np += 1
        if df['despidos'][i] == 'No, pero lo está considerando':
            nc += 1
        if df['despidos'][i] == 'No, pero lo va a hacer en los próximos días':
            npd += 1
        if df['despidos'][i] == 'Sí':
            si += 1
    names = ['Sí','No','No, pero lo está considerando','No cuenta con personal','No, pero lo va a hacer en los próximos días']
    result = [si, no, np, nc, npd]

    if df.empty:
        fig = px.pie(values=0, names="No hay datos", hole=0.4, title='No hay datos');
        return fig

    fig = po.Figure(data=[po.Pie(labels=names, values=result, hole=.4)])
    colors = ['#FAEBD7', '#CDC0B0', '#FFE4C4', '#8B7D6B', '#DEB887']
    fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(title_text="Porcentaje de empresas que han despedido personal", font=dict(size=10))

    return fig

def creditoGraphic(sector, municipio, giro):
    user_input = sector
    df = filterdf(sector, municipio, giro)# codigo que filtra --- este es para las graficas
    data = filterdata(sector, municipio, giro)# codigo que filtra ---- este es para las metricas
    if df.empty:
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No existe información con los filtros seleccionados",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }
    si=0
    no = 0
    cons = 0
    ya=0

    if len(data) == None:
        print("Esta vacio")
        fig = px.pie(values=0, names="No hay datos", hole=0.4, title='No hay datos');
        return fig

    for i in range(0, len(data)):
        if df['credito_solicitud'][i] == 'Sí':
            si += 1
        if df['credito_solicitud'][i] == 'No':
            no += 1
        if df['credito_solicitud'][i] == 'Lo estoy considerando':
            cons += 1
        if df['credito_solicitud'][i] == 'Ya lo hice':
            ya += 1

    fig = po.Figure(data=[po.Pie(labels=['Sí', 'No', 'Lo estoy considerando', 'Ya lo hice'],
                                 values=[si, no, cons, ya],
                                 hole=.4)])
    colors = ['#8FBC8F', '#228B22', '#C1FFC1', '#698B69']
    fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(title_text="Porcentaje de empresas que tomarían algún tipo de crédito para tener mayor liquidez", font=dict(size=10))
    return fig   

def insumosGraphic(sector, municipio, giro):
    df = filterdf(sector, municipio, giro) # codigo que filtra --- este es para las graficas
    data = filterdata(sector, municipio, giro)# codigo que filtra ---- este es para las metricas
    if df.empty:
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No existe información con los filtros seleccionados",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }
    si=0
    no = 0
    nose=0
    for i in range(0, len(data)):
        if df['aumento_insumos'][i] == 'Sí':
            si += 1
        if df['aumento_insumos'][i] == 'No':
            no += 1
        if df['aumento_insumos'][i] == 'No sé':
            nose += 1

    if df.empty:
        fig = px.pie(values=0, names="No hay datos", hole=0.4, title='No hay datos');
        return fig

    fig = po.Figure(data=[po.Pie(labels=['Sí', 'No', 'No sé'],
                                 values=[si, no, nose],
                                 hole=.4)])
    colors = ['#8B7500', '#DAA520', '#FFEC8B']
    fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(title_text="Porcentaje de empresas que han observado aumentos en los costos de su operación", font=dict(size=10))
    return fig       

def preciosGraphic(sector, municipio, giro):
    df = filterdf(sector, municipio, giro) # codigo que filtra --- este es para las graficas
    data = filterdata(sector, municipio, giro)# codigo que filtra ---- este es para las metricas
    if df.empty:
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No existe información con los filtros seleccionados",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }
    si=0
    no = 0
    na=0
    nc=0
    cons=0
    for i in range(0, len(data)):
        if df['aumento_precios'][i] == 'Sí':
            si += 1
        if df['aumento_precios'][i] == 'No':
            no += 1
        if df['aumento_precios'][i] == 'No aplica':
            na += 1
        if df['aumento_precios'][i] == 'No contesto':
            nc += 1
        if df['aumento_precios'][i] == 'No, pero lo estoy considerando':
            cons += 1

    if df.empty:
        fig = px.pie(values=0, names="No hay datos", hole=0.4, title='No hay datos');
        return fig

    fig = po.Figure(data=[po.Pie(labels=['Sí', 'No', 'No aplica', 'No contestó', 'No, pero lo está considerando'],
                                 values=[si, no, na, nc, cons],
                                 hole=.4)])
    colors = ['#FFA07A', '#FFB6C1', '#FA8072', 'cadetblue', '#E9967A']
    fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(title_text="Porcentaje de empresas que han tenido que subir precios para compensar mayores costos", font=dict(size=10))
    return fig     

def porcentajeGraphic(sector, municipio, giro):
    df = filterdf(sector, municipio, giro)# codigo que filtra --- este es para las graficas
    if df.empty:
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No existe información con los filtros seleccionados",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }
    ventas = list(df['ventas_porcentaje'])
    ventas = list(filter(lambda a: a != 997, ventas))
    ventas = list(filter(lambda a: a != 998, ventas))
    ventas = list(filter(lambda a: a != 999, ventas))

    a = Counter(ventas)
    f = sorted(list(a.items()))

    arange = {'0-20%': np.sum([f[i][1] for i in range(len(f)) if f[i][0] <= 20]),
              '21-40%': np.sum([f[i][1] for i in range(len(f)) if 20 < f[i][0] <= 40]),
              '41-60%': np.sum([f[i][1] for i in range(len(f)) if 40 < f[i][0] <= 60]),
              '61-80%': np.sum([f[i][1] for i in range(len(f)) if 60 < f[i][0] <= 80]),
              '80-100%': np.sum([f[i][1] for i in range(len(f)) if 80 < f[i][0] <= 100])}

    labels = list(arange.keys())
    values = list(arange.values())

    fig = po.Figure([po.Bar(x=labels, y=values, marker_color='rgb(55, 83, 109)')])
    fig.update_layout(title_text='Porcentaje de reducción de ventas', xaxis=dict(title='Porcentaje de reducción'),
                      yaxis=dict(title='Cantidad de empresas'))
    fig.update_layout(font=dict(size=10))
    return fig     
