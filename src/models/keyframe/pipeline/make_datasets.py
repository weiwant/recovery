"""
@Author: Wenfeng Zhou
"""
import json
from pathlib import Path

import h5py
import numpy as np
from tqdm import tqdm

from src.models.keyframe.utils import video
from src.models.keyframe.utils.config import get_config


def main(args):
    # create output directory
    out_dir = Path(args.save_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # annotation directory
    label_dir = Path(args.label_dir)

    # feature extractor
    print('Loading feature extractor ...')
    video_proc = video.VideoPreprocessor(args.sample_rate)

    # search all videos with .mp4 suffix
    video_paths = sorted(Path(args.video_dir).glob('*.mp4'))
    print(f'Processing {len(video_paths)} videos ...')

    with h5py.File(args.save_path, 'w') as h5out:
        for idx, video_path in tqdm(list(enumerate(video_paths))):
            n_frames, features, cps, nfps, picks = video_proc.run(video_path)

            # load labels
            video_name = video_path.stem
            label_path = label_dir / f'{video_name}.json'
            with open(label_path) as f:
                data = json.load(f)
            user_summary = np.array(data['user_summary'], dtype=np.float32)
            _, label_n_frames = user_summary.shape
            assert label_n_frames == n_frames, f'Invalid label of size {len(gtscore)}: expected {n_frames}'

            # compute ground truth frame scores
            gtscore = np.mean(user_summary[:, ::args.sample_rate], axis=0)

            # write dataset to h5 file
            video_key = f'video_{idx}'
            h5out.create_dataset(f'{video_key}/features', data=features)
            h5out.create_dataset(f'{video_key}/gtscore', data=gtscore)
            h5out.create_dataset(f'{video_key}/user_summary', data=user_summary)
            h5out.create_dataset(f'{video_key}/change_points', data=cps)
            h5out.create_dataset(f'{video_key}/n_frame_per_seg', data=nfps)
            h5out.create_dataset(f'{video_key}/n_frames', data=n_frames)
            h5out.create_dataset(f'{video_key}/picks', data=picks)
            h5out.create_dataset(f'{video_key}/video_name', data=video_name)

    print(f'Dataset saved to {args.save_path}')


if __name__ == '__main__':
    config = get_config(config_mode='datasets')
    main(config)
