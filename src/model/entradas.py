
# .. ................................................................................... .. #
# .. Proyecto: UrbanLab - Plataforma de ayuda para micro y pequeñas empresas             .. #
# .. Archivo: entrada.py - diccionario con datos de entrada                              .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                  .. #
# .. Licencia: Todos los derechos reservados                                             .. #
# .. Repositorio: https://github.com/IFFranciscoME/Urban_Lab.git                         .. #
# .. ................................................................................... .. #

# -- BASES DE DATOS --

# Datos de MiPyMEs
path_data_pyme = 'Base_de_datos.xlsx'
sheet_data_pyme = 'IIEG_E_1'

# Datos de Precios
path_data_prices = 'Precios_INEGI.xlsx'
sheet_data_prices = 'Datos_acomodados'

# GeoDatos de coordenadas por CP
shp_path = "cp_jal_2\\CP_14_Jal_v2.shp"
kml_path = "cp_jal_2\\CP_14_Jal_v2.kml"

# -- ------------------------------------------------------------------------------------ -- #
# -- Entrada para metrica de estres
# -- ------------------------------------------------------------------------------------ -- #
#Definir el valor de cada variable que compone pagos
p_esp = .15
p_gen = .1

conditions_stress = {
				'ventas_porcentaje': {
							1: (-1, 25),
							2: (25, 50),
							3: (50, 75),
							4: (75, 100)
						},
				'perdidas_porcentaje': {
							1: (-1, 25),
							2: (25, 50),
							3: (50, 75),
							4: (75, 150) # 992
						},
				'capacidad': {
							1: (-1, 25),
							2: (25, 50),
							3: (50, 75),
							4: (75, 100)
						},
				'cerrar': {
							0: ['No'],
							2: ['Sí']
						},
				'despidos': {
							2: ['Sí', 'No, pero lo está considerando'],
							0: ['No', 'No cuenta con personal'],
							3: ['No, pero lo va a hacer en los próximos días']
						},
				'plantilla_porcentaje': {
							1: (-1, 25),
							2: (25, 50),
							3: (50, 75),
							4: (75, 100)
						},
				'pago_salarios': {
							0: [100, 101, 102],
							p_esp*4: (-1, 6),
							p_esp*3: (6, 12),
							p_esp*2: (12, 18),
							p_esp*-1: (18, 52) # 367
						},
				'pago_impuestos': {
							0: [100, 101, 102],
							p_gen*4: (-1, 6),
							p_gen*3: (6, 12),
							p_gen*2: (12, 18),
							p_gen*-1: (18, 52) # 82
						},
				'pago_créditos': {
							0: [100, 101, 102],
							p_gen*4: (-1, 6),
							p_gen*3: (6, 12),
							p_gen*2: (12, 18),
							p_gen*-1: (18, 52)
						},
				'pago_renta': {
							0: [100, 101, 102],
							p_gen*4: (-1, 6),
							p_gen*3: (6, 12),
							p_gen*2: (12, 18),
							p_gen*-1: (18, 52)
						},
				'pago_internet': {
							0: [100, 101, 102],
							p_gen*4: (-1, 6),
							p_gen*3: (6, 12),
							p_gen*2: (12, 18),
							p_gen*-1: (18, 52)
						},
				'pago_agua': {
							0: [100, 101, 102],
							p_gen*4: (-1, 6),
							p_gen*3: (6, 12),
							p_gen*2: (12, 18),
							p_gen*-1: (18, 52)
						},
				'pago_luz': {
							0: [100, 101, 102],
							p_gen*4: (-1, 6),
							p_gen*3: (6, 12),
							p_gen*2: (12, 18),
							p_gen*-1: (18, 52)
						},
				'pago_gas': {
							0: [100, 101, 102],
							p_gen*4: (-1, 6),
							p_gen*3: (6, 12),
							p_gen*2: (12, 18),
							p_gen*-1: (18, 52)
						},
				'duración': {
							0: [100, 101, 102],
							p_esp*4: (-1, 6),
							p_esp*3: (6, 12),
							p_esp*2: (12, 18),
							p_esp*-2: (18, 24)
						},
				'capacidad_pago': {
							2: ['No'],
							1: ['Sí'],
							0: ['No sé']
						},
				'crédito': {
							0: ['No'],
							2: ['Sí']
						},
				'aumento_insumos': {
							0: ['No'],
							3: ['Sí']
						},
				'aumento_precios': {
							0: ['No'],
							1: ['No, pero lo estoy considerando'],
							3: ['Sí']
						} ,
				'escasez_insumos': {
							0: ['No'],
							3: ['Sí']
						} ,
				'aumento_tipocambio': {
							0: ['No'],
							4: ['Sí']
						}
				}
				
				
# -- ------------------------------------------------------------------------------------ -- #
# -- Entrada para metrica de adaptabilidad
# -- ------------------------------------------------------------------------------------ -- #				
conditions_adaptability = {
				'capacidad': {
							1: (-1, 50),
							2: (50, 100)
						},
				'cerrar_razon': {
							1: ['Falta de fondos o liquidez', 'Gastos elevados', 
								   'Problemas con importaciones o exportaciones', 
								   'Problemas de cobranza'],
							0: [100, 'Incertidumbre sobre la duración de la caída en ventas',
								   'Otro (Por favor especifique)', 
								      'Multas del gobierno de la emergencia sanitaria', 
									  'Depende del turismo'] ### else
						},
				'despidos': {
							0: ['Sí', 'No cuenta con personal', 
								   'No, pero lo va a hacer en los próximos días'],
							2: ['No'],
							1: ['No, pero lo está considerando']
						},
				'pago_salarios': {
							0: [100, 101, 102],
							1: (-1, 12),
							2: (12, 52)
						},
				'capacidad_pago': {
							0: ['No'],
							2: ['Sí'],
							1: ['No sé']
						},
				'acuerdo_laboral': {
							0: ['No'],
							1: ['No, pero lo está considerando', 
								   'No, pero lo va a hacer en los próximos días'],
							2: ['Sí']
						},
				'trabajo_casa': {
							0: ['No', 100],
							1: ['No, pero lo está considerando', 
								   'No, pero lo va a hacer en los próximos días'],
							2: ['Sí']
						},
				'trabajo_casa_motivo': {
							1: ['La naturaleza de mi negocio no lo permite', 
							      'Porque se considera una actividad esencial para la emergencia'],
					        0: ['Otro (Por favor especifique)', 
								 'No me convence la modalidad de trabajar desde casa', 100]
						},
				'aumento_precios': {
							0: ['No'],
							1: ['No, pero lo estoy considerando'],
							2: ['Sí']
						}
				}


dict_conditions = { 'Estres': conditions_stress, 'Adaptabilidad': conditions_adaptability}
dict_colors = { 'Estres': "Reds", 'Adaptabilidad': "Purp"}

