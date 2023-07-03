# -*- coding: utf-8 -*-
import json
import os.path
from os import listdir

import h5py
import numpy as np

from src.models.keyframe.utils.config import get_config
from src.models.keyframe.utils.summary import generate_summary, evaluate_summary


def main(args):
    # arguments to run the scrip
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

    # Save the importance scores in json format.
    with open(path + '/f_scores.json', 'w') as outfile:
        json.dump(f_score_epochs, outfile)


if __name__ == '__main__':
    config = get_config(config_mode='evaluate')
    main(config)
