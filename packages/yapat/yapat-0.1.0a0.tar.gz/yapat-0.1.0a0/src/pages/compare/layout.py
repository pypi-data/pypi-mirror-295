import logging

import dash
import dash_bootstrap_components as dbc
from dash import html

# from .callbacks import scan_projects
from .. import login_required_layout

logger = logging.getLogger(__name__)

dash.register_page(
    __name__,
    path='/compare',
    title='Compare | YAPAT'
)

layout = html.H1('Compare')