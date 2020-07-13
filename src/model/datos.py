
# .. ................................................................................... .. #
# .. Proyecto: UrbanLab - Plataforma de ayuda para micro y pequeñas empresas             .. #
# .. Archivo: datos.py - procesos de obtencion y almacenamiento de datos                 .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                  .. #
# .. Licencia: Todos los derechos reservados                                             .. #
# .. Repositorio: https://github.com/IFFranciscoME/Urban_Lab.git                         .. #
# .. ................................................................................... .. #

import pandas as pd
import numpy as np
import model.entradas as ent
from model.proceso import metric_quantification, semaforo_precios
from config.config import db

class Data():

	# -- -------------------------------------------------------------------------------- -- #
	# -- Read data file and storing it in df_data
	# -- -------------------------------------------------------------------------------- -- #
	def get_data(self):
		self.df_pymes = pd.read_excel(db + 'Base_de_datos.xlsx', sheet_name='IIEG_E_1')
		self.df_prices = pd.read_excel(db + 'Precios_INEGI.xlsx', sheet_name='Datos_acomodados')
		
	# -- -------------------------------------------------------------------------------- -- #
	# -- Limpiar base de datos de las PyMEs
	# -- -------------------------------------------------------------------------------- -- #
	@staticmethod
	def clean_data_pymes(df_pymes):
        # Replace
		
		df = df_pymes.copy()
		df.replace([998, 999, 'No contesto', 'No sé'], np.nan, inplace=True)
		df.replace(
            {
                "Más de 52": 52,
                "De 26 a 52": 26,
                "No aplica": 100,
                "No contesto": 101,
                "No sé": 102,
                "Más de un año": 12}, inplace=True)

        # Specific columns
		df['aumento_precios'].replace(100, np.nan, inplace=True)
		# Tomar solo la ZMG
		df_final = df.loc[df['Municipio'].isin(['Zapopan','Tonalá','Tlaquepaque',
												'Tlajomulco de Zúñiga','El Salto','Guadalajara'])]
		# Reiniciar el index
		df_final.reset_index(drop=True, inplace=True)
		return df_final


	# -- -------------------------------------------------------------------------------- -- #
	# -- Limpiar base de datos de los precios
	# -- -------------------------------------------------------------------------------- -- #
	@staticmethod
	def clean_data_prices(df_prices):
		"""
			Funcion que limpia especificamente los datos de los precios

		    Parameters
		    ---------
		    df_prices: DataFrame : datos que se encuentran en un DataFrame

		    Returns
		    ---------
		    df: DataFrame : datos limpios

		    Debuggin
		    ---------
			df_data = read_file('Precios_INEGI.xlsx', 'Datos_acomodados')

			"""
		# Hacer copia
		df = df_prices.copy()

		# Quitar numeros innecesarios
		def col_no_numb(df):
			# De las columnas
			col_n = ['División', 'Grupo', 'Clase']
			# Quitar numeros
			no_numb = [df[i].str.replace('\d+', '') for i in col_n]
			# Quitar punto y espacio inicial
			for i in range(len(col_n)):
				point = ['. ', '.. ', '... ']
				df[col_n[i]] = no_numb[i].str.replace(point[i], '', regex=False)
			return df

		df = col_no_numb(df)

		# Nombre de todas las columnas con precios acomodadas correctamente
		col_df = list(df.columns)[::-1][0:22]

		# Merge ciertas columnas de original con las diferencias
		df_new = pd.merge(
			df[['División', 'Grupo', 'Clase', 'Generico', 'Especificación']],
			df[col_df].iloc[:, 1:],
			left_index=True, right_index=True)

		return df_new

# -- ----------------------------------------------------------------------------------- -- #
# -- Datos que se necesitan y calculos de metricas
# -- ----------------------------------------------------------------------------------- -- #
# Datos que se utilizaran
data = Data()
data.get_data()

# limpiar base de datos
df_pymes = data.clean_data_pymes(data.df_pymes)

# -- Estres --
metric_s = metric_quantification(df_pymes, ent.conditions_stress, 'Estres')

# Dataframe de metrica de estres
df_stress = metric_s['df_prices']
# tabla de metrica
metric_s_table = metric_s['metric_table']

# -- Adaptabilidad
metric_a = metric_quantification(df_pymes, ent.conditions_adaptability, 'Adaptabilidad')

# Dataframe de metrica de estres
df_adapt = metric_a['df_prices']
# tabla de metrica
metric_a_table = metric_a['metric_table']

# Diccionario
dict_metrics_df = {'Estres': df_stress, 'Adaptabilidad': df_adapt}
dict_metrics_table = {'Estres': metric_s_table, 'Adaptabilidad': metric_a_table}

# -- ----------------------------------------------------------------------------------- -- #

# limpiar base de datos
df_prices = data.clean_data_prices(data.df_prices)

# Semaforo
#dict_semaforo = semaforo_precios(df_prices)

# Dataframe multi index (grupos | clases)
#predicciones = dict_semaforo['predicciones']
#predicciones.to_pickle("predicciones.pkl")
predicciones = pd.read_pickle(db + "predicciones.pkl")

# Dalaframe con semaforo
#semaforo = dict_semaforo['semaforo']
#semaforo.to_pickle("semaforo.pkl")
semaforo = pd.read_pickle(db + "semaforo.pkl")
