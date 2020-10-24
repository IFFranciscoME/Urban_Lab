import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app.client.utils.header import header
from app.client.utils.body import body
from app.client.utils.footer import footer
from app.client.utils.header_filter import header_filter
from app.client.utils.body_filter import body_filter



layout = html.Div([ 
    header,
    body,
    footer
], className='d-flex flex-column align-items-start')

layout_filter = html.Div([ 
    header_filter,
    body_filter,
    footer
], className='d-flex flex-column align-items-start')