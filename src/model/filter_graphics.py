# Importar librerias
import plotly.express as px
import plotly.graph_objects as go
import geojson
import pandas as pd
import numpy as np
from collections import Counter

import dash_core_components as dcc

data_c = pd.read_excel('./src/db/data.xlsx', sheet_name = 'BD_Monitoreo')
df_c = data_c.filter(items = ['Sector', 'Municipio', 'Giro','ventas_porcentaje',
                         'despidos', 'credito', 'credito_solicitud', 'aumento_insumos',
                          'aumento_precios'])


def optionslct(data):
    return df_c[data].unique()


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
    fig = px.pie(values = result, names=names, hole = 0.4, title = 'Despidos')

    return fig

def creditoGraphic(sector, municipio, giro):
    user_input = sector
    df = filterdf(sector, municipio, giro)# codigo que filtra --- este es para las graficas
    data = filterdata(sector, municipio, giro)# codigo que filtra ---- este es para las metricas
    si=0
    no = 0
    cons = 0
    ya=0
    for i in range(0, len(data)):
        if df['credito_solicitud'][i] == 'Sí':
            si += 1
        if df['credito_solicitud'][i] == 'No':
            no += 1
        if df['credito_solicitud'][i] == 'Lo estoy considerando':
            cons += 1
        if df['credito_solicitud'][i] == 'Ya lo hice':
            ya += 1

    fig = px.pie(values = [si, no,cons,ya], names=['Sí','No','Lo estoy considerando','Ya lo hice'], hole = 0.4, title = 'Solicitud de Crédito')

    return fig   

def insumosGraphic(sector, municipio, giro):
    df = filterdf(sector, municipio, giro) # codigo que filtra --- este es para las graficas
    data = filterdata(sector, municipio, giro)# codigo que filtra ---- este es para las metricas
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
            
    fig = px.pie(values = [si, no, nose], names=['Sí','No','No sé'], hole = 0.4, title = 'Aumento de insumos')

    return fig       

def preciosGraphic(sector, municipio, giro):
    df = filterdf(sector, municipio, giro) # codigo que filtra --- este es para las graficas
    data = filterdata(sector, municipio, giro)# codigo que filtra ---- este es para las metricas
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
            
    fig = px.pie(values = [si, no,na,nc,cons], names=['Sí','No','No aplica','No contestó','No, pero lo está considerando'], hole = 0.4, title = 'Aumento de precios')

    return fig     

def porcentajeGraphic(sector, municipio, giro):
    df = filterdf(sector, municipio, giro)# codigo que filtra --- este es para las graficas
    ventas = list(df['ventas_porcentaje'])
    ventas =list(filter(lambda a: a != 997, ventas))
    ventas =list(filter(lambda a: a != 998, ventas))
    ventas =list(filter(lambda a: a != 999, ventas))

    a = Counter(ventas)
    f =sorted(list(a.items()))

    labels, values = zip(*f)
    indexes = np.arange(len(labels))
    width = 0.8
    fig = px.bar(values, x=labels, y=values, title = 'Porcentaje de afectación de ventas')

    return fig     
