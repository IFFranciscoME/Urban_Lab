# .. ................................................................................... .. #
# .. Proyecto: UrbanLab - Plataforma de ayuda para micro y pequeñas empresas             .. #
# .. Archivo: proceso.py - funciones de procesamiento general de datos                   .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                  .. #
# .. Licencia: Todos los derechos reservados                                             .. #
# .. Repositorio: https://github.com/IFFranciscoME/Urban_Lab.git                         .. #
# .. ................................................................................... .. #


# Importar librerias
import math
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

import statistics
import statsmodels.api as sm
from scipy.stats import shapiro
from statsmodels.stats.diagnostic import het_arch
from statsmodels.stats.diagnostic import acorr_ljungbox

from sklearn.metrics import r2_score
from sklearn import linear_model
from itertools import chain


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Calcular metrica con diccionario
# -- ------------------------------------------------------------------------------------ -- #
def metric_quantification(p_df_data, p_conditions, p_metric):
    """
	Funcion que pasa un diccionario con condiciones por columna al dataframe de pymes
	que regresa la suma de la metrica de acuerdo a las condiciones que se le de

    Parameters
    ---------
    p_df_data: DataFrame : datos de pymes en Dataframe
	p_conditions: dict : diccionario con condiciones
	p_metric: str : nombre de la metrica

    Returns
    ---------
    df: dict : Diccionario con metrica en el df original y como matriz

    Debuggin
    ---------
	p_df_data = datos.clean_data_pymes((datos.read_file(
							'Base_de_datos.xlsx', 'IIEG_E_1'))
	p_conditions = entradas.conditions_stress
	p_metric = 'Estres'

	"""
    # Nombre de columnas
    list_columns = list(p_conditions.keys())
    # Condiciones (dicts)
    list_dict_conditions = list(p_conditions.values())
    # Lista de lista con resultados
    answer = [[round(
        f_condition(
		    list_dict_conditions[k],
            p_df_data[list_columns[k]][i]
        ),
    3)
        for i in range(len(p_df_data))
    ]
        for k in range(len(list_columns))
    ]
    # DataFrame con la matriz de todo
    metric = pd.DataFrame(answer)

    # --------------------------
    # Columna con suma
    metric_sum = round(metric.sum(), 3)

    # Nombre de variables para columnas
    col = list(p_conditions.keys())

    # Transponer tabla de metrica
    metric_table = metric.T

    # Asignar nombres a las columnas
    metric_table.columns = col

    # Agregar columna de suma total
    metric_table['Total'] = metric_sum

    # --------------------------

    # Dataframe copia
    df = p_df_data.copy()

    # Dataframe con columna de metrica
    df[p_metric] = metric_sum

    return {'df_prices': df, 'metric_table': metric_table}


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Regresa el resultado de un dato de acuerdo a las condiciones
# -- ------------------------------------------------------------------------------------ -- #
def f_condition(p_dict_condition, p_data):
    """
	Funcion que checa en el diccionario de condiciones para las metricas
	el diccionario de condiciones contiene dentro otros diccionarios, donde:
		el value del dict dentro del dict es p_codition (la condicion que se debe de cumplir)
		y el key es el resultado que se asigna si cumple la condicion
	esto lo checa para cada dato de acuerdo a la columna (key del dict) en otra funcion

    Parameters
    ---------
    p_dict_condition: dict : diccionario con condiciones
	p_data: int or str: dato a comparar

	Returns
    ---------
    int: valor de acuerdo a la condicion

    Debuggin
    ---------
	p_dict_condition = list(entradas.conditions_stress.values())[0]
	p_data = datos.clean_data_pymes((datos.read_file(
							'Base_de_datos.xlsx', 'IIEG_E_1'))['ventas_porcentaje'][0]

	"""
    # Valores que se podrian poner
    posible_results = list(p_dict_condition.keys())

    # lista de condiciones
    list_conditions = list(p_dict_condition.values())

    # Utilizando la funcion para cada condicion
    answer = [f_type_verification(list_conditions[i], posible_results[i],
                                  p_data) for i in range(len(list_conditions))]

    # Si todos son cero, quiere decir que p_data es nan
    if answer == [0] * len(answer):
        return 0

    # Si no
    else:
        # Quitar los nan de la lista answer
        lista = list(filter(None.__ne__, answer))
        if len(lista) == 0:
            return np.nan
        else:
            # Regresar el resultado
            return lista[0]


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Checar la condicion de acuerdo a su tipo
# -- ------------------------------------------------------------------------------------ -- #
def f_type_verification(p_condition, p_result, p_data):
    """
	Funcion que de acuerdo a los 3 parametros te regresa un resultado,
		p_data puede ser string o int, pero si p_condition es una lista se busca en tal
		si esta se devuelve p_result, si p_data no es string entonces es numerico
		si es nan devuelve 0 si es tupla, debe de estar entre ambos numeros de la tupla

    Parameters
    ---------
    p_condition: tuple or list : contiene las condiciones
	p_result: int : numero si se cumple la condicion es el resultado
	p_data: int or str: dato que se esta comparando para cuantificar

    Returns
    ---------
    p_result: int : numero de la metrica

    Debuggin
    ---------
	p_condition = (0, 25)
	p_result = 1
	p_data = 10

	"""
    # Si es lista tiene que estar en tal
    if type(p_condition) == list:
        if p_data in p_condition:
            return p_result

    # Si es numerico
    if type(p_data) != str:
        if math.isnan(p_data):
            return 0
        # Si es tuple, tiene que estar entre ambos numeros
        if type(p_condition) == tuple:
            if p_condition[0] < p_data and p_data <= p_condition[1]:
                return p_result


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Separar series de tiempo del data frame de precios
# -- ------------------------------------------------------------------------------------ -- #
def f_time_series(p_df_prices, p_clase):
    """
    Funcion que separa las serie de tiempo de acuerdo a la clase que se le pida

    Parameters
    ---------
    p_df_prices: DataFrame : data en un DF
    p_clase: str : clase que se requieren los productos

    Returns
    ---------
    series_tiempo: list : todas las series de tiempo

    Debuggin
    ---------
    p_df_prices = read_file('Precios_INEGI.xlsx', 'Datos_acomodados')
    p_clase = 'Accesorios y utensilios'

    """
    # Agrupar por clase
    clases = list(p_df_prices.groupby('Clase'))

    # Busqueda de dataframe para la clase que se necesita
    search = [clases[i][1] for i in range(len(clases)) if clases[i][0] == p_clase][0]
    search.reset_index(inplace=True, drop=True)

    # Agrupar por generico
    generico = list(search.groupby('Generico'))

    # Series de tiempo por Generico
    series_tiempo = [generico[i][1].median().rename(generico[i][0],
                                                    inplace=True) for i in range(len(generico))]

    return series_tiempo


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: lista de grupos con cada clase de productos
# -- ------------------------------------------------------------------------------------ -- #
def f_clases(p_df_prices):
    """
    Funcion que regresa una lista con el nombre de todos los grupos y dentro de la misma
    otra lista con el nombre de todas las clases por grupo

    Parameters
    ---------
    p_df_data: DataFrame : data en un DataFrame

    Returns
    ---------
    list_clases: list : todas las clases por grupo

    Debuggin
    ---------
    p_df_prices = read_file('Precios_INEGI.xlsx', 'Datos_acomodados')

    """
    # Separar por grupo
    group_by_group = list(p_df_prices.groupby('Grupo'))

    # lista por grupo y clases por grupo
    list_clases = [[grupo[0], grupo[1]['Clase'].unique().tolist()] for grupo in group_by_group]

    return list_clases


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Predecir serie de tiempo
# -- ------------------------------------------------------------------------------------ -- #
def f_predict_time_series(p_serie_tiempo):
    """
	Funcion que modela una serie de tiempo utilizando desde una regresion lineal hasta
	un modelo sarima con metodo de box jenkins para predecir cual seria el cambio
	en los precios

    Parameters
    ---------
    p_serie_tiempo: DataFrame : serie de tiempo a modelar

    Returns
    ---------
    cambio_porc: float : cambio porcentual del ultimo precio a el que se predice

    Debuggin
    ---------
	p_serie_tiempo = datos.clean_data_prices(
							datos.read_file('Precios_INEGI.xlsx', 'Datos_acomodados'))

	"""

    # Meses en el futuro, predecir
    meses = 6

    # Ultimo precio
    ultimo_precio = p_serie_tiempo[len(p_serie_tiempo) - 1]

    # Reiniciar indice
    serie_tiempo = p_serie_tiempo.copy()
    serie_tiempo.reset_index(drop=True, inplace=True)

    # ------------------------------------------ #
    # Primero: intentar con una regresión lineal
    # ------------------------------------------ #

    # Separar la informacion que se tiene de la serie de tiempo en y
    y_o = np.array(serie_tiempo)
    x_o = np.arange(len(serie_tiempo))

    # Acomodarla de la forma que el modelo necesita
    x = x_o.reshape((len(x_o), 1))
    y = y_o.reshape((len(y_o), 1))

    # Crear el modelo
    modelo = linear_model.LinearRegression()

    # Pasar nuestros datos por el modelo
    modelo.fit(x, y)

    # De acuerdo al modelo, calcular y
    y_pred = modelo.predict(x)

    # R2 de sus residuales
    r_2 = r2_score(y, y_pred)

    if r_2 > 0.9:
        # sumar a la x ultima
        value = x_o[-1] + meses
        # predecir
        prediction = modelo.predict(value.reshape((1, 1)))
        # cambio porcentual
        cambio_porc = (ultimo_precio - prediction[0][0]) / ultimo_precio

        return cambio_porc

    else:
        # ------------------------------------------ #
        # Segundo: intentar modelar con ARIMA
        # ------------------------------------------ #

        # Empezar checando si es estacionaria
        def check_stationarity(data):
            # Usar dicky fuller
            test_results = sm.tsa.stattools.adfuller(data)
            # Cuando se cumple esto es estacionaria la serie orginal
            if test_results[0] < 0 and test_results[1] <= 0.05:
                lags = 0

            # Cuando no se cumple se debe diferenciar para que sea estacionaria
            else:
                for i in range(3):
                    # Diferenciar datos
                    new_data = np.diff(data)

                    # Volver a calcular test dicky fuller
                    new_results = sm.tsa.stattools.adfuller(new_data)

                    # Volver a comparar para decidir si es o no estacionaria
                    if new_results[0] < 0 and new_results[1] <= 0.05:
                        # rezagos necesarios para volverlo estacionario
                        lags = i
                        break

                    else:
                        data = new_data
                        # solo permitimos 3 rezagos, si aún no lo es, no se modela
                        lags = np.nan
            return lags

        # Checar estacionariedad
        d = check_stationarity(serie_tiempo)

        if np.isnan(d):
            return 0

        else:

            # lambda para tomar los coef significativos
            all_significant_coef = lambda x: x if abs(x) > 0.5 else None

            def significat_lag(all_coef):
                # Tomar los indices de los rezagos
                ind_c = all_coef.index.values
                # Solo los rezagos menores a 7
                sig_i = ind_c[ind_c < 7]
                # Nuevos coeficientes
                new_coef = all_coef[all_coef.index.isin(list(sig_i))]
                if len(new_coef) > 1:
                    # Tomar los valores absolutos
                    abs_coef = new_coef[1:].abs()
                    # Buscar el maximo
                    max_coef = abs_coef.max()
                    # El indice es el rezago al que pertenece
                    answer = abs_coef[abs_coef == max_coef[0]].dropna().index[0]
                    return answer
                else:
                    return 1

            # Calcular coeficientes de fac parcial
            facp = sm.tsa.stattools.pacf(serie_tiempo)

            # Pasar lambda y quitar los que no son significativos
            p_s = pd.DataFrame(all_significant_coef(facp[i]) for i in range(len(facp))).dropna()

            # Tomar el primero que sea signiticativo, sera la p de nuestro modelo
            p = significat_lag(p_s)

            # --- #

            # Calcular coeficientes de fac
            fac = sm.tsa.stattools.acf(serie_tiempo, fft=False)

            # Pasar lambda y quitar los que no son significativos
            q_s = pd.DataFrame(all_significant_coef(fac[i]) for i in range(len(fac))).dropna()

            # Tomar el primero que sea signiticativo, sera la p de nuestro modelo
            q = significat_lag(q_s)

            # Modelo
            arima = sm.tsa.statespace.SARIMAX(serie_tiempo,
                                              order=(p, d, q),
                                              trend='c',
                                              enforce_stationarity=True,
                                              enforce_invertibility=True)
            arima_fitted = arima.fit()

            def check_resid(model_fit):
                # estadístico Ljung – Box.
                colineal = acorr_ljungbox(model_fit.resid, lags=[10])
                # se necesita aceptar H0, es decir p_value debe ser mayor a .05
                colin = True if colineal[1] > 0.05 else False

                # shapiro test
                normalidad = shapiro(model_fit.resid)
                # si el p-value es menor a alpha, rechazamos la hipotesis de normalidad
                norm = True if normalidad[1] > 0.05 else False

                # arch test
                heterosced = het_arch(model_fit.resid)
                # p-value menor a 0.05 y concluir que no hay efecto de heteroscedasticidad
                heter = True if heterosced[1] > 0.05 else False

                return colin, norm, heter

            # test en los residuales
            resid_test = check_resid(arima_fitted)

            # predecir siguientes 6 meses
            future_prices = arima_fitted.forecast(meses, alpha=0.05)

            # Prediccion
            prediction = future_prices[len(serie_tiempo) + meses - 1]

            cambio_porc = (ultimo_precio - prediction) / ultimo_precio

            if abs(cambio_porc) < 0.4 and True in resid_test:
                return cambio_porc

            else:
                return np.nan


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Predecir todas las series de una clase
# -- ------------------------------------------------------------------------------------ -- #
def f_predict_clase(df_prices, clase):
    """
	Funcion que regresa todas las predicciones

    Parameters
    ---------
    df_data: DataFrame : datos limpios de precios
	p_clase: str : clase que se requieren la prediccion

    Returns
    ---------
    med_predict: float : porcentaje medio de la clase

    Debuggin
    ---------
	df_data = df_prices
	p_clase = 'Accesorios y utensilios'

	"""
    # Fragmentar por series de tiemo
    time_series = f_time_series(df_prices, clase)

    # Predicciones de la clase (por producto)
    predictions = [f_predict_time_series(time_series[s]) for s in range(len(time_series))]

    # Series
    df_predict = pd.Series(predictions)
    df_predict.rename(clase, inplace=True)

    return df_predict


# -- ------------------------------------------------------------------------------------ -- #
# -- Function: Predecir todas las clases de todos los grupos y generar el semaforo
# -- ------------------------------------------------------------------------------------ -- #
def semaforo_precios(df_prices):
    """
	Funcion que genera el dataframe de los precios con ayuda de las funciones:
		f_predict_clase y a su vez f_predict_time_series

    Parameters
    ---------
    df_data: DataFrame : datos limpios de precios

    Returns
    ---------
    med_predict: float : porcentaje medio de la clase

    Debuggin
    ---------
	df_data = df_prices

	"""
    # Clases del dataframe por grupo
    grupo_clases = f_clases(df_prices)

    # Solo nombres de clases
    clases_all = [
        [grupo_clases[i][1][j] for j in range(len(
            grupo_clases[i][1]))
         ] for i in range(len(grupo_clases))
    ]

    # Medias de predicciones
    predictions = [
        [f_predict_clase(df_prices, clases_all[i][j]
                         ).median() for j in range(len(clases_all[i]))
         ] for i in range(len(clases_all))
    ]

    # Ultimos precios
    last_prices = [
        [round(df_prices[df_prices['Clase'] == clases_all[i][j]
                         ]['may 2020'].median(), 2) for j in range(len(clases_all[i]))
         ] for i in range(len(clases_all))
    ]

    # Precios futuros
    pred_prices = [[[
        last_prices[i][j],
        round(last_prices[i][j] * (1 + predictions[i][j]), 4)
    ]
        for j in range(len(clases_all[i]))
    ] for i in range(len(clases_all))
    ]

    # Nombres de indices
    tuplas_2d = [[(grupo_clases[i][0], grupo_clases[i][1][j]) for j in range(len(grupo_clases[i][1]))
                  ] for i in range(len(grupo_clases))]
    # Aplanar lista
    tuplas = list(chain.from_iterable(tuplas_2d))

    # Generar el multi index
    ind = pd.MultiIndex.from_tuples(tuplas)

    # Valores para DataFrame
    values = np.array(list(chain.from_iterable(pred_prices)))

    # Dataframe con precios
    df = pd.DataFrame(values, index=ind)

    cols = ['Ultimo precio', 'Precio para Nov 2020']
    df.columns = cols

    # Crear tabla
    semaforo = pd.DataFrame()
    for i in range(len(grupo_clases)):
        mean_group = statistics.median(predictions[i])
        if mean_group < -0.01:
            result = 'verde'
        elif mean_group > 0.01:
            result = 'rojo'
        else:
            result = 'amarillo'
        semaforo[grupo_clases[i][0]] = [result, round(mean_group * 100, 3)]

    return {'semaforo': semaforo.T, 'predicciones': df}
