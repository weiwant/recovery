import os

import h5py

from src.models.keyframe.utils.config import get_config


def main(args):
    save_path = args["save_path"]
    datasets = args.get("datasets", None)
    all_datasets = args["all"]
    datasets_dir = './datasets/keyframe/'
    datasets_list = list(filter(lambda x: x.endswith('.h5') and 'mix' not in x, os.listdir(datasets_dir)))
    if datasets:
        datasets_list = list(filter(lambda x: any([d.lower() in x for d in datasets]), datasets_list))
    else:
        if not all_datasets:
            print('No datasets specified. Use --all to combine all datasets.')
            return

    with h5py.File(save_path, 'w') as h5out:
        idx = 0
        for dataset in datasets_list:
            dataset_path = os.path.join(datasets_dir, dataset)
            hdf = h5py.File(dataset_path, 'r')
            for video_key in hdf:
                features = hdf.get(f'{video_key}/features')
                gtscore = hdf.get(f'{video_key}/gtscore')
                user_summary = hdf.get(f'{video_key}/user_summary')
                cps = hdf.get(f'{video_key}/change_points')
                nfps = hdf.get(f'{video_key}/n_frame_per_seg')
                n_frames = hdf.get(f'{video_key}/n_frames')
                picks = hdf.get(f'{video_key}/picks')
                video_name = hdf.get(f'{video_key}/video_name')
                h5out.create_dataset(f'video_{idx}/features', data=features)
                h5out.create_dataset(f'video_{idx}/gtscore', data=gtscore)
                h5out.create_dataset(f'video_{idx}/user_summary', data=user_summary)
                h5out.create_dataset(f'video_{idx}/change_points', data=cps)
                h5out.create_dataset(f'video_{idx}/n_frame_per_seg', data=nfps)
                h5out.create_dataset(f'video_{idx}/n_frames', data=n_frames)
                h5out.create_dataset(f'video_{idx}/picks', data=picks)
                if video_name:
                    h5out.create_dataset(f'video_{idx}/video_name', data=video_name)
                idx += 1
            hdf.close()


if __name__ == '__main__':
    config = get_config(config_mode='combine')
    main(config)
