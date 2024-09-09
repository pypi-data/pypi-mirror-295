import glob
import json
import logging
import os

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

config = json.load(open('config.json'))


def _read_embeddings(self):
    embeddings = np.load(self.path_embeddings)
    return embeddings


def read_annotations(path_annotations=None, manual_col_prefix='species_', col_processed='processed',
                     col_skipped='skipped', species_classes=['Amphibia', 'Aves', 'Insecta', 'Mammalia', 'Others']):
    path_annotations = path_annotations or config.get('PATH_ANNOTATIONS')
    if os.path.exists(path_annotations):
        # load annotations
        annotations = pd.read_csv(path_annotations)
    else:
        # detections = read_detections()
        # create dictionary with necessary columns

        all_wavs = glob.glob(config['PATH_AUDIO'])

        annotations_dict = {
            # 'path_sample': detections['path_sample'],
            # 'basename': detections['path_sample'].apply(lambda x: os.path.splitext(os.path.basename(x))[0]),
            col_processed: 0,
            col_skipped: 0
        }

        # create dataframe
        annotations = pd.DataFrame(annotations_dict)

    # cols to int
    columns_to_int = [col for col in annotations.columns
                      if col.startswith(manual_col_prefix) or col == col_processed]
    for col in columns_to_int:
        annotations[col] = annotations[col].replace('', np.nan)
        annotations[col] = annotations[col].astype(float)

    return annotations


# def get_next_file_properties(self, selected_audio='raw'):
#     self._update_file_properties()
#     if selected_audio == 'raw':
#         audio = self.audio
#     else:
#         audio = self.concatenated_audio
#     return self.annotations.loc[self.file_index, 'basename'], audio


# def _update_file_properties(self):
#     # delete all indices from queue that are already annotated
#     # TODO Vectorize operation
#     self.file_index_queue = [tup for tup in self.file_index_queue if
#                              self.annotations.loc[tup[0], self.col_processed] != 1 and
#                              self.annotations.loc[tup[0], self.col_skipped] != 1]
#
#     # derive next file index from sampling queue
#     if not self.file_index_queue:
#         self.sampling(sampling_strategy='random', ignore_current_processes=True)
