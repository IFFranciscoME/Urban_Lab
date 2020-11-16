
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Urban Lab / Laboratorio de econometría espacial urbana - PAP4J05                           -- #
# -- script: dash.py : script con el codigo funcional del dashboard                                      -- #
# -- author: FranciscoME / PAP4J05                                                                       -- #
# -- license: MIT                                                                                        -- #
# -- repository: https://github.com/IFFranciscoME/Urban_Lab_App                                          -- #
# -- --------------------------------------------------------------------------------------------------- -- #

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from config import config
from api.server import server

app = dash.Dash(name=config.name,
                server=server,
                routes_pathname_prefix='/',
                assets_folder=config.assets,
                external_stylesheets=[dbc.themes.BOOTSTRAP, config.fontawesome], 
                suppress_callback_exceptions = True)


app_form = dash.Dash(name=config.name,
                server=server,
                routes_pathname_prefix='/formEconomic/',
                assets_folder=config.assets,
                external_stylesheets=[dbc.themes.BOOTSTRAP, config.fontawesome],
                suppress_callback_exceptions = True)



from app.client.layouts.layout import layout

from app.client.layouts.layout import layout_form

app.title = config.name

app.layout = layout



app_form.title = config.name

app_form.layout = layout_form

