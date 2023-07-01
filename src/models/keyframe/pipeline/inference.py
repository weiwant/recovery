# -*- coding: utf-8 -*-
import argparse
import json
import os
from os import listdir
from os.path import isfile, join

import h5py
import numpy as np
import torch

from src.models.keyframe.framework.model import PGL_SUM
from src.models.keyframe.utils.summary import generate_summary, evaluate_summary


def inference(model, data_path, keys, eval_method):
    """ Used to inference a pretrained `model` on the `keys` test videos, based on the `eval_method` criterion; using
        the dataset located in `data_path'.

        :param nn.Module model: Pretrained model to be inferenced.
        :param str data_path: File path for the dataset in use.
        :param list keys: Containing the test video keys of the used data split.
        :param str eval_method: The evaluation method in use {SumMe: max, TVSum: avg}
    """
    model.eval()
    video_fscores = []
    for video in keys:
        video = os.path.basename(video)
        with h5py.File(data_path, "r") as hdf:
            # Input features for inference
            frame_features = torch.Tensor(np.array(hdf[f"{video}/features"])).view(-1, 1024)
            # Input need for evaluation
            user_summary = np.array(hdf[f"{video}/user_summary"])
            sb = np.array(hdf[f"{video}/change_points"])
            n_frames = np.array(hdf[f"{video}/n_frames"])
            positions = np.array(hdf[f"{video}/picks"])

        with torch.no_grad():
            scores, _ = model(frame_features)  # [1, seq_len]
            scores = scores.squeeze(0).cpu().numpy().tolist()
            summary = generate_summary([sb], [scores], [n_frames], [positions])[0]
            f_score = evaluate_summary(summary, user_summary, eval_method)
            video_fscores.append(f_score)
    print(f"Trained for split: {split_id} achieved an F-score of {np.mean(video_fscores):.2f}%")


if __name__ == "__main__":
    # arguments to run the script
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default='SumMe', help="Dataset to be used. Supported: {SumMe, TVSum}")
    parser.add_argument("--method", type=str, default='avg', help="Evaluation method to be used. Supported: {avg, max}")

    args = vars(parser.parse_args())
    dataset = args["dataset"]
    eval_metric = args["method"]
    models_path = os.path.join('./models/keyframe', dataset)
    for split_id in range(len(os.listdir(models_path))):
        # Model data
        model_path = os.path.join(models_path, f"split{split_id}")
        model_file = [f for f in listdir(model_path) if isfile(join(model_path, f))]

        # Read current split
        split_file = os.path.join('./datasets/keyframe/splits', next(
            filter(lambda x: dataset.lower() in x, os.listdir('./datasets/keyframe/splits'))))
        with open(split_file) as f:
            data = json.loads(f.read())
            test_keys = data[split_id]["test_keys"]

        # Dataset path
        dataset_path = os.path.join('./datasets/keyframe',
                                    next(filter(lambda x: dataset.lower() in x, os.listdir('./datasets/keyframe'))))

        # Create model with paper reported configuration
        trained_model = PGL_SUM(input_size=1024, output_size=1024, num_segments=4, heads=8,
                                fusion="add", pos_enc="absolute")
        trained_model.load_state_dict(torch.load(join(model_path, model_file[-1])))
        inference(trained_model, dataset_path, test_keys, eval_metric)
