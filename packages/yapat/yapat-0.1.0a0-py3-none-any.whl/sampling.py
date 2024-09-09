import json
import logging
import os
import random
import time
from pathlib import Path

import librosa
import numpy as np

# from .model import create_model_mil, train_model
from src import utils, models

logger = logging.getLogger(__name__)

config = json.load(open('config.json'))


def sampling(annotations, sampling_start_time, sampling_strategy=None, path_audio=config.get('PATH_AUDIO'),
             ignore_current_processes=False):

    # write log message to the screen
    # queue_too_long = False
    # if queue_too_long:
    #     logger.info(f"Queue too long with {len(foo)} samples. Not drawing a new sample at this time.")

    # check the number of processes (allow only 4 at a time)
    if not ignore_current_processes:
        # get current time
        time_now = np.round(time.time(), 2)
        # kill processes after 60 seconds timeout
        sampling_start_time = [start_time if time_now - start_time < 60 else 0
                               for start_time in sampling_start_time]
        # start sampling with current strategy if spot available
        if 0 in sampling_start_time:
            process_index = sampling_start_time.index(0)
            sampling_start_time[process_index] = time_now
        else:
            return None, sampling_start_time

    # select sampling strategy
    if not sampling_strategy:
        # sampling_strategy = self.sampling_strategy
        logger.info("No sampling strategy specified. Returning random.")
        sampling_strategy = 'random'

    # TODO Revise sampling strategy based on these criteria
    # if len(indices_labelled) < 10:
    #     return _sampling_validation()
    # elif not training_columns:
    #     return _sampling_random()

    # get next sample with defined sampling strategy
    if sampling_strategy == 'random':
        sampled_index = _random(annotations)
    elif sampling_strategy == 'validate':
        detections = app_utils.read_detections()
        sampled_index = _validation(annotations, detections)
    elif sampling_strategy == 'refine':
        raise NotImplementedError
        sampled_index = _refine()
    elif sampling_strategy == 'discover':
        raise NotImplementedError
        sampled_index = _discover()
    else:
        logger.info(f'Sampling strategy {sampling_strategy} not recognized. Returning random')
        sampled_index = _random()

    # TODO: comment next line before deploying
    # sampled_index = 0
    # load file path
    file_path = Path(path_audio, annotations.loc[sampled_index, 'path_sample'])

    # load audio
    normalized_audio, _ = librosa.load(file_path, sr=48000)

    # read basename
    basename = annotations.loc[sampled_index, 'basename']
    # find all files with the basename
    audio_file_paths = []
    for root, _, files in os.walk(path_audio):
        for file in files:
            if basename in os.path.basename(file):
                current_file_path = os.path.join(root, file)
                audio_file_paths.append(current_file_path)
    # create concatenated file
    audio_arrays = []
    for audio_file_path in audio_file_paths:
        audio, _ = librosa.load(audio_file_path, sr=48000)
        # scale audio loudness
        audio = audio / max(0.01, np.max(np.abs(audio)))
        audio_arrays.append(audio)
    audio_concatenated = np.concatenate(audio_arrays)

    # append index, file path and audio as tuple to queue
    sampled_tuple = (sampled_index, file_path, normalized_audio, audio_concatenated)

    # # check if process was not killed
    if not ignore_current_processes:
        if sampling_start_time[process_index] != time_now:
            return None, None
        else:
            sampling_start_time[process_index] = 0

    # # append sampled item to queue
    # self.file_index_queue.append(sampled_tuple)

    return sampled_tuple, sampling_start_time


def _random(annotations, col_processed='processed', col_skipped='skipped'):
    # unprocessed_mask = (annotations[col_processed] != 1) & (annotations[col_skipped] != 1)
    ndx = annotations.loc[:, [col_processed, col_skipped]].values.any(1) == False
    return random.choice(annotations.loc[ndx, :].index)


def _validation(annotations, detections, competence_classes=None, sampling_selected_species=None,
                manual_col_prefix='species_', col_processed='processed', col_skipped='skipped'):
    # get all species columns
    species_columns = [col for col in annotations.columns if col.startswith(manual_col_prefix) and
                       any(col.startswith(comp_class) for comp_class in competence_classes)]
    species_columns = [s.replace(manual_col_prefix, '', 1) for s in species_columns]

    # drop species that are detected 5 or more times
    species_to_drop = []
    # TODO Vectorize
    for col in species_columns:
        if annotations[manual_col_prefix + col].sum() >= 5:
            species_to_drop.append(col)
    species_columns = list(set(species_columns) - set(species_to_drop))

    # drop species that are manually excluded
    species_columns = list(set(species_columns) - set(sampling_selected_species))

    # no species column in competence class
    if not species_columns:
        logger.info("No categories found for validation. Returning random sample.")
        # TODO Define indices_to_sample within scope of validation()
        raise NotImplementedError
        return random(indices_to_sample)

    # get df with relevant columns
    columns_to_keep = [col for col in detections.columns if any(sub in col for sub in species_columns)]
    relevant_detections = detections[columns_to_keep].copy()

    # get def with relevant rows
    unprocessed_mask = (annotations[col_processed] != 1) & (annotations[col_skipped] != 1)
    relevant_detections = relevant_detections[unprocessed_mask]

    # get index of highest score
    max_value = relevant_detections.values.max(axis=1)
    row_index = np.random.choice(len(max_value), p=max_value / max_value.sum())
    return row_index


def _refine(annotations, embeddings, competence_classes=None, sampling_selected_species=None,
            manual_col_prefix='species_', col_processed='processed', col_skipped='skipped'):
    # divide embeddings in labelled and unlabelled samples
    indices_labelled = annotations.index[annotations[col_processed] == 1].tolist()
    indices_unlabelled = annotations.index[annotations[col_processed] == 0].tolist()

    if not sampling_selected_species:
        # exclude all species columns not optimised for
        training_columns = [col for col in annotations.columns if col.startswith(manual_col_prefix) and
                            any(comp_class in col for comp_class in competence_classes)]
    else:
        # use only selected species for active learning
        training_columns = [manual_col_prefix + s for s in sampling_selected_species]

    # # if less than 10 samples are labelled, choose other sampling method
    # TODO Move this decision to sampling()
    # if len(indices_labelled) < 10:
    #     return _sampling_validation()
    # elif not training_columns:
    #     return _sampling_random()

    # get metadata
    training_df = annotations.loc[indices_labelled, training_columns]
    y_train = training_df.to_numpy()
    # get training and sampling data
    x_train = embeddings[indices_labelled, :]
    x_sample = embeddings[indices_unlabelled, :]

    # create a model with num_species outputs
    # model = create_model(x_train, y_train)
    model = models.create_model_mil(shape=x_train.shape[1:], units=len(training_columns))

    # train model on labelled data
    models.train_model(model, x_train, y_train)

    # apply model to unlabelled data
    y_pred_sample = model(x_sample).numpy()

    # get uncertainty score for unlabelled data
    uncert_ratio = 1 / (0.5 + np.abs(y_pred_sample - 0.5)) - 1
    uncert_ratio_max = np.max(uncert_ratio, axis=1)
    uncert_ratio_max -= uncert_ratio_max.min()

    # softmax selection
    sampled_embedding_index = np.random.choice(len(uncert_ratio_max), p=uncert_ratio_max / uncert_ratio_max.sum())
    sampled_index = indices_unlabelled[sampled_embedding_index]

    return sampled_index


def _discover(annotations, embeddings, competence_classes=None, sampling_selected_species=None,
              manual_col_prefix='species_', col_processed='processed', col_skipped='skipped'):
    # divide embeddings in labelled and unlabelled samples
    indices_labelled = annotations.index[annotations[col_processed] == 1].tolist()
    indices_unlabelled = annotations.index[annotations[col_processed] == 0].tolist()

    # exclude all species columns not optimised for
    training_columns = [col for col in annotations.columns if col.startswith(manual_col_prefix) and
                        any(comp_class in col for comp_class in competence_classes)]

    # # if less than 10 samples are labelled, choose other sampling method
    # if len(indices_labelled) < 10:
    #     return _sampling_validation()
    # elif not training_columns:
    #     return _sampling_random()

    # get metadata
    training_df = annotations.loc[indices_labelled, training_columns]
    y_train = training_df.to_numpy()
    # get training and sampling data
    x_train = embeddings[indices_labelled, :]
    x_sample = embeddings[indices_unlabelled, :]

    # detection model: get y labels
    y_sampled_species_present = y_train.any(1)
    # detection model: create model
    model_detection = create_model_mil(shape=x_train.shape[1:], units=1)
    # detection model: train model
    train_model(model_detection, x_train, y_sampled_species_present)
    # detection model: get predictions
    y_pred_detection = model_detection(x_sample)
    y_pred_detection = np.max(y_pred_detection, axis=1)

    # identification model: get y labels
    indices_present_classes = np.nonzero(np.sum(y_train, axis=0))[0]
    y_sampled_nonempty_classes = y_train[:, indices_present_classes]
    # identification model: create model
    model_classification = models.create_model_mil(shape=x_train.shape[1:], units=len(indices_present_classes))
    # identification model: train model
    models.train_model(model_classification, x_train, y_sampled_nonempty_classes)
    # identification model: get predictions
    y_pred_classification = model_classification(x_sample)
    y_pred_classification_max = np.max(y_pred_classification, axis=1)

    # score combination (most certain a detection + most certain no classification)
    sample_score = y_pred_detection * (1 - y_pred_classification_max)
    logit_sample_score = np.log(sample_score / (1 - sample_score))
    logit_sample_score -= logit_sample_score.min()
    logit_sample_score /= logit_sample_score.sum()

    # softmax selection
    sampled_embedding_index = np.random.choice(len(sample_score), p=logit_sample_score)
    sampled_index = indices_unlabelled[sampled_embedding_index]
    return sampled_index
