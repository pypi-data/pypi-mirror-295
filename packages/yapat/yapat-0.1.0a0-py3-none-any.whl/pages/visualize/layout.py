import logging

import dash
import dash_bootstrap_components as dbc
from dash import html

# from .callbacks import scan_projects
from .. import login_required_layout

logger = logging.getLogger(__name__)

dash.register_page(
    __name__,
    path='/vis',
    redirect_from=['/visualise', '/visualize', '/viz'],
    title='Visualize | YAPAT'
)

layout = html.H1('Visualize')