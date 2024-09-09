import glob
import logging
import os
from datetime import datetime
from multiprocessing import Pool

import dash
import numpy as np
import pandas as pd
import tensorflow as tf
from dash import html, callback, Input, Output, State, dcc

from pages import get_list_files, split_single_audio, load_audio_files_with_tf_dataset

logger = logging.getLogger(__name__)


def scan_projects():
    """
    Scan the existing projects
    """
    options = ([{'label': x, 'value': x} for x in os.listdir('projects') if
                os.path.isdir(os.path.join('projects', x))])
    return options


def init_project(project_name, audio_path, clip_duration, embedding_model):
    """
    Initializes the project by generating clips, tables, queue, and embeddings.
    """
    try:
        logging.info(f'Initializing project {project_name}')
        os.makedirs(os.path.join('projects', project_name), exist_ok=True)
        gen_tables(project_name)
        gen_clips(project_name, audio_path, clip_duration)
        gen_queue(project_name, n=10)
        gen_embeddings(project_name, embedding_model)
    except Exception as e:
        logger.error(f"Failed to initialize project '{project_name}': {str(e)}")
        raise


def gen_clips(project_name, audio_path, clip_duration):
    """
    Generates audio clips for the project.
    """
    path_clips = os.path.join('projects', project_name, 'clips')
    os.makedirs(path_clips, exist_ok=True)
    list_files = get_list_files(audio_path)
    logging.info(f'Generating audio clips for project {project_name} with {len(list_files)} audio files')
    with Pool() as pool:
        pool.starmap(split_single_audio, [(file, path_clips, clip_duration) for file in list_files])


def gen_tables(project_name):
    """
    Generates the initial vocabulary and annotations files for the project.
    """
    logging.info(f'Generating initial vocabulary and annotations files for project {project_name}')
    with open(os.path.join('projects', project_name, 'vocabulary.txt'), 'x') as f:
        os.utime(f.fileno(), None)

    annotations = pd.DataFrame({
        'sound_clip_url': [],
        'label': [],
        'timestamp': []
    }, index=pd.Index([], name='id'))
    annotations.to_csv(os.path.join('projects', project_name, 'annotations.csv'))


def gen_queue(project_name, n=5):
    """
    Generates a queue of audio clips to be annotated.
    """
    all_clips = glob.glob(os.path.join('projects', project_name, 'clips', '*.wav'))
    n = min(n, len(all_clips))
    logging.info(f'Generating queue of {n} audio clips for project {project_name}')
    try:
        sound_clip_url = np.random.choice(all_clips, n, replace=False)
        queue = pd.DataFrame({
            'sound_clip_url': [os.path.basename(p) for p in sound_clip_url],
            'status': 'pending',
            'method': 'random',
            # 'priority': 0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }, index=pd.Index(range(n), name='id'))
        queue.to_csv(os.path.join('projects', project_name, 'queue.csv'))
    except Exception as e:
        logger.error(f"Error generating queue for project '{project_name}': {str(e)}")
        raise


def gen_embeddings(project_name, embedding_model):
    """
    Generates embeddings for the audio clips in the project.
    """
    logging.info(f'Generating embeddings for project {project_name}')
    all_clips = glob.glob(os.path.join('projects', project_name, 'clips', '*.wav'))

    try:
        if embedding_model == 'birdnet':
            model = tf.keras.layers.TFSMLayer('assets/models/BirdNET-Analyzer-V2.4/V2.4/BirdNET_GLOBAL_6K_V2.4_Model',
                                              call_endpoint='embeddings')
            sr = 48000
        else:
            raise ValueError(f"Unknown embedding model: {embedding_model}")

        audio_dataset = load_audio_files_with_tf_dataset(all_clips, sample_rate=sr)
        results = tf.keras.Sequential([model]).predict(audio_dataset.batch(128), verbose=2)

        embeddings_df = pd.DataFrame(
            index=[os.path.basename(file) for file in all_clips],
            data=results['embeddings']
        )

        embeddings_df.to_pickle(os.path.join('projects', project_name, 'embeddings.pkl'))
    except Exception as e:
        logger.error(f"Error generating embeddings for project '{project_name}': {str(e)}")
        raise


# %%
@callback(
    Output('project-list', 'options'),
    Output('project-list', 'value'),
    Output('project-content', 'data', allow_duplicate=True),
    Input('project-list', 'value'),
    Input('button-project-create', 'n_clicks'),
    State('navbar', 'brand'),
    State('project-name', 'value'),
    State('audio-path', 'value'),
    State('embedding-model', 'value'),
    State('project-content', 'data'),
    prevent_initial_call=True
)
def update_options_project(project_value, project_create, brand, project_name, audio_path, embedding_model, data):
    if dash.ctx.triggered_id == 'button-project-create':
        clip_duration = 3 if embedding_model == 'birdnet' else None  # Clip duration in seconds
        project_value = project_name
        init_project(project_name, audio_path, clip_duration, embedding_model)
        # TODO Queue initialization tasks, inform when ready
    elif data.get('project_name') and not project_value:
        project_value = data['project_name']

    options = scan_projects()
    data['project_name'] = project_value
    data['current_sample'] = ''

    return options, project_value, data


@callback(
    Output('project-summary', 'children'),
    Input('project-list', 'value')
)
def update_project_summary(project_name):
    children = [html.H5('Project summary')]
    if project_name:
        all_clips = glob.glob(os.path.join('projects', project_name, 'clips', '*.wav'))
        annotations = pd.read_csv(os.path.join('projects', project_name, 'annotations.csv'))
        n_labeled = len(annotations['sound_clip_url'].unique())
        n_classes = len(annotations.columns)
        children.append(html.P(f'Found {len(all_clips)} clips, {n_labeled} of which are labelled for {n_classes} class categories'))
        children.append(dcc.Link("Start annotating", href='/annotate'))
        children.append(html.P('Export project data'))
    return children


@callback(
    Output('button-project-create', 'disabled'),
    Input('project-name', 'valid'),
    Input('audio-path', 'valid'),
    Input('embedding-model', 'valid'),
)
def check_create(v1, v2, v3):
    return not (v1 and v2 and v3)


@callback(
    Output("collapse", "is_open"),
    Input("collapse-button", "n_clicks"),
    Input("button-project-cancel", "n_clicks"),
    State("collapse", "is_open"),
)
def toggle_collapse(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@callback(
    Output('project-name', 'valid'),
    Output('project-name', 'invalid'),
    Input('project-name', 'value')
)
def check_project_name(value):
    if value:
        is_valid = value not in os.listdir('projects')
        return is_valid, not is_valid
    return False, False


@callback(
    Output('audio-path', 'valid'),
    Output('audio-path', 'invalid'),
    Input('audio-path', 'value')
)
def check_audio_path(value):
    if value:
        is_valid = os.path.isdir(os.path.abspath(value))
        return is_valid, not is_valid
    return False, False


@callback(
    Output('embedding-model', 'valid'),
    Output('embedding-model', 'invalid'),
    Input('embedding-model', 'value')
)
def check_embedding_model(value):
    if value:
        return True, False
    return False, False

# layout = html.Div([
#     html.Label('Select project'),
#     dcc.Dropdown(
#         id='project-list-dropdown',
#         options=[{'label': 'True', 'value': 'True'}, {'label': 'False', 'value': 'False'}],
#         # value=debug_mode
#     ),
#
#     html.H1('Environment Variable Control Panel'),
#
#     html.Label('Debug Mode'),
#     dcc.Dropdown(
#         id='debug-dropdown',
#         options=[{'label': 'True', 'value': 'True'}, {'label': 'False', 'value': 'False'}],
#         # value=debug_mode
#     ),
#
#     html.Label('Database URL'),
#     dcc.Input(
#         id='database-url-input',
#         type='text',
#         # value=database_url,
#         style={'width': '100%'}
#     ),
#
#     html.Label('API Key'),
#     dcc.Input(
#         id='api-key-input',
#         type='text',
#         # value=api_key,
#         style={'width': '100%'}
#     ),
#
#     html.Button('Save Changes', id='save-button', n_clicks=0),
#
#     html.Div(id='save-status')
# ])


#
# #
# #
# # @app.callback(
# #     Output('save-status', 'children'),
# #     [Input('save-button', 'n_clicks')],
# #     [State('debug-dropdown', 'value'),
# #      State('database-url-input', 'value'),
# #      State('api-key-input', 'value')]
# # )
# # def update_env_file(n_clicks, debug_value, db_url_value, api_key_value):
# #     if n_clicks > 0:
# #         # Update the .env file
# #         set_key('.env', 'DEBUG', debug_value)
# #         set_key('.env', 'DATABASE_URL', db_url_value)
# #         set_key('.env', 'API_KEY', api_key_value)
# #
# #         return 'Environment variables updated!'
# #     return ''
# #
