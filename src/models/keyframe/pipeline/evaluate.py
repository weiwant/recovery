# -*- coding: utf-8 -*-
import argparse
import json
import os.path
from os import listdir
from typing import Any, List

import h5py
import numpy as np


def knapSack(W, wt, val, n):
    """ Maximize the value that a knapsack of capacity W can hold. You can either put the item or discard it, there is
    no concept of putting some part of item in the knapsack.

    :param int W: Maximum capacity -in frames- of the knapsack.
    :param list[int] wt: The weights (lengths -in frames-) of each video shot.
    :param list[float] val: The values (importance scores) of each video shot.
    :param int n: The number of the shots.
    :return: A list containing the indices of the selected shots.
    """
    K: List[Any] = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Build table K[][] in bottom up manner
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w:
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    selected = []
    w = W
    for i in range(n, 0, -1):
        if K[i][w] != K[i - 1][w]:
            selected.insert(0, i - 1)
            w -= wt[i - 1]

    return selected


def generate_summary(all_shot_bound, all_scores, all_nframes, all_positions):
    """ Generate the automatic machine summary, based on the video shots; the frame importance scores; the number of
    frames in the original video and the position of the sub-sampled frames of the original video.

    :param list[np.ndarray] all_shot_bound: The video shots for all the -original- testing videos.
    :param list[np.ndarray] all_scores: The calculated frame importance scores for all the sub-sampled testing videos.
    :param list[np.ndarray] all_nframes: The number of frames for all the -original- testing videos.
    :param list[np.ndarray] all_positions: The position of the sub-sampled frames for all the -original- testing videos.
    :return: A list containing the indices of the selected frames for all the -original- testing videos.
    """
    all_summaries = []
    for video_index in range(len(all_scores)):
        # Get shots' boundaries
        shot_bound = all_shot_bound[video_index]  # [number_of_shots, 2]
        frame_init_scores = all_scores[video_index]
        n_frames = all_nframes[video_index]
        positions = all_positions[video_index]

        # Compute the importance scores for the initial frame sequence (not the sub-sampled one)
        frame_scores = np.zeros(n_frames, dtype=np.float32)
        if positions.dtype != int:
            positions = positions.astype(np.int32)
        if positions[-1] != n_frames:
            positions = np.concatenate([positions, [n_frames]])
        for i in range(len(positions) - 1):
            pos_left, pos_right = positions[i], positions[i + 1]
            if i == len(frame_init_scores):
                frame_scores[pos_left:pos_right] = 0
            else:
                frame_scores[pos_left:pos_right] = frame_init_scores[i]

        # Compute shot-level importance scores by taking the average importance scores of all frames in the shot
        shot_imp_scores = []
        shot_lengths = []
        for shot in shot_bound:
            shot_lengths.append(shot[1] - shot[0] + 1)
            shot_imp_scores.append((frame_scores[shot[0]:shot[1] + 1].mean()).item())

        # Select the best shots using the knapsack implementation
        final_shot = shot_bound[-1]
        final_max_length = int((final_shot[1] + 1) * 0.15)

        selected = knapSack(final_max_length, shot_lengths, shot_imp_scores, len(shot_lengths))

        # Select all frames from each selected shot (by setting their value in the summary vector to 1)
        summary = np.zeros(final_shot[1] + 1, dtype=np.int8)
        for shot in selected:
            summary[shot_bound[shot][0]:shot_bound[shot][1] + 1] = 1

        all_summaries.append(summary)

    return all_summaries


def evaluate_summary(predicted_summary, user_summary, eval_method):
    """ Compare the predicted summary with the user defined one(s).

    :param ndarray predicted_summary: The generated summary from our model.
    :param ndarray user_summary: The user defined ground truth summaries (or summary).
    :param str eval_method: The proposed evaluation method; either 'max' (SumMe) or 'avg' (TVSum).
    :return: The reduced fscore based on the eval_method
    """
    max_len = max(len(predicted_summary), user_summary.shape[1])
    S = np.zeros(max_len, dtype=int)
    G = np.zeros(max_len, dtype=int)
    S[:len(predicted_summary)] = predicted_summary

    f_scores = []
    for user in range(user_summary.shape[0]):
        G[:user_summary.shape[1]] = user_summary[user]
        overlapped = S & G

        # Compute precision, recall, f-score
        precision = sum(overlapped) / sum(S)
        recall = sum(overlapped) / sum(G)
        if precision + recall == 0:
            f_scores.append(0)
        else:
            f_scores.append(2 * precision * recall * 100 / (precision + recall))

    if eval_method == 'max':
        return max(f_scores)
    else:
        return sum(f_scores) / len(f_scores)


def main():
    # arguments to run the script
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str,
                        required=True,
                        help="Path to the json files with the scores of the frames for each epoch")
    parser.add_argument("--dataset", type=str, default='SumMe', help="Dataset to be used")
    parser.add_argument("--eval", type=str, default="max",
                        help="Eval method to be used for f_score reduction (max or avg)")

    args = vars(parser.parse_args())
    path = args["path"]
    dataset = args["dataset"]
    eval_method = args["eval"]

    results = [f for f in listdir(path) if f.endswith(".json")]
    results.sort(key=lambda video: int(video[6:-5]))
    dataset_path = os.path.join('./datasets/keyframe',
                                next(filter(lambda x: dataset.lower() in x, os.listdir('./datasets/keyframe'))))

    f_score_epochs = []
    for epoch in results:  # for each epoch ...
        all_scores = []
        with open(path + '/' + epoch) as f:  # read the json file ...
            data = json.loads(f.read())
            keys = list(data.keys())

            for video_name in keys:  # for each video inside that json file ...
                scores = np.asarray(data[video_name])  # read the importance scores from frames
                all_scores.append(scores)

        all_user_summary, all_shot_bound, all_nframes, all_positions = [], [], [], []
        with h5py.File(dataset_path, 'r') as hdf:
            for video_name in keys:
                video_index = video_name[6:]

                user_summary = np.array(hdf.get('video_' + video_index + '/user_summary'))
                sb = np.array(hdf.get('video_' + video_index + '/change_points'))
                n_frames = np.array(hdf.get('video_' + video_index + '/n_frames'))
                positions = np.array(hdf.get('video_' + video_index + '/picks'))

                all_user_summary.append(user_summary)
                all_shot_bound.append(sb)
                all_nframes.append(n_frames)
                all_positions.append(positions)

        all_summaries = generate_summary(all_shot_bound, all_scores, all_nframes, all_positions)

        all_f_scores = []
        # compare the resulting summary with the ground truth one, for each video
        for video_index in range(len(all_summaries)):
            summary = all_summaries[video_index]
            user_summary = all_user_summary[video_index]
            f_score = evaluate_summary(summary, user_summary, eval_method)
            all_f_scores.append(f_score)

        f_score_epochs.append(np.mean(all_f_scores))
        print("f_score: ", np.mean(all_f_scores))

    # Save the importance scores in txt format.
    with open(path + '/f_scores.txt', 'w') as outfile:
        json.dump(f_score_epochs, outfile)


if __name__ == '__main__':
    main()
