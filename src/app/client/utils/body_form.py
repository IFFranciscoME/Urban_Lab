import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

body_form = html.Div([
html.Div([
    html.Div([
        html.H1(children=["Cuestionario de recopilación de datos"], style={'display': 'inline-block', "marginTop": "20px"}),
        html.Form([
            html.P(children=[
                "¿Ha tenido que subir precios para compensar mayores costos?",
                dcc.RadioItems(options=[
                {'label': 'Si', 'value': 'Si'},
                {'label': 'No', 'value': 'No'},
                {'label': 'No aplica', 'value': 'No aplica'},
                {'label': 'Prefiero no contestar', 'value': 'No contesto'},
                {'label': 'No, pero lo estoy considerando', 'value': 'No, pero lo estoy considerando'}
            ],
                labelStyle={'display': 'block'})
            ]),
            html.P(children=[
                "¿Ha observado aumentos en los costos de su operación?",
                dcc.RadioItems(options=[
                    {'label': 'Sí', 'value': 'Sí'},
                    {'label': 'No', 'value': 'No'},
                    {'label': 'No sé', 'value': 'No sé'}
                ],
                    labelStyle={'display': 'block'})
            ]),
            html.P(children=[
                "¿Tomaría algún tipo de crédito para tener mayor liquidez ante la pandemia de COVID-19?",
                dcc.RadioItems(options=[
                    {'label': 'Sí', 'value': 'Sí'},
                    {'label': 'No', 'value': 'No'},
                    {'label': 'Lo estoy considerando', 'value': 'Lo estoy considerando'},
                    {'label': 'Ya lo hice', 'value': 'Ya lo hice'}
                ],
                    labelStyle={'display': 'block'})
            ]),
            html.P(children=[
                "¿Su establecimiento se ha visto en la necesidad de despedir personal?",
                dcc.RadioItems(options=[
                    {'label': 'No', 'value': 'No'},
                    {'label': 'No cuento con personal', 'value': 'No cuenta con personal'},
                    {'label': 'No, pero lo estoy considerando', 'value': 'No, pero lo está considerando'},
                    {'label': 'Ya lo hice', 'value': 'Ya lo hice'}
                ],
                    labelStyle={'display': 'block'})
            ]),
            html.P(children=[
                "¿En qué porcentaje aproximadamente vio reducidas sus ventas?",
                dcc.Slider(min=0, max=100, step=1, value=100)
            ])

        ])
        ], className=" col-sm-6 col-md-6 col-lg-9 col-xl-9", style={'backgroundColor': '#F9F9F9'})
    ], className='row justify-content-center', style={'backgroundColor': '#F2F2F2', "marginTop": "20px", "marginBottom": "20px"})
], className="container", style={'backgroundColor': '#F2F2F2'})
