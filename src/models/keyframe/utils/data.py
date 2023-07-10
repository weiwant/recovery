"""
@Author: Wenfeng Zhou
"""
import json
import os

import h5py
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader


class VideoData(Dataset):
    def __init__(self, mode, video_type, split_index):
        """ Custom Dataset class wrapper for loading the frame features and ground truth importance scores.

        :param str mode: The mode of the model, train or test.
        :param str video_type: The Dataset being used, SumMe or TVSum.
        :param int split_index: The index of the Dataset split being used.
        """
        self.mode = mode
        self.name = video_type.lower()
        self.datasets_base = './datasets/keyframe'
        self.datasets = list(filter(lambda x: x.endswith('.h5'), os.listdir(self.datasets_base)))
        self.splits_filename = list(
            filter(lambda x: self.name in x, os.listdir(os.path.join(self.datasets_base, 'splits'))))
        self.split_index = split_index  # it represents the current split (varies from 0 to 4)

        self.filename = os.path.join(self.datasets_base, next(filter(lambda x: self.name in x, self.datasets)))
        hdf = h5py.File(self.filename, 'r')
        self.list_frame_features, self.list_gtscores = [], []

        with open(os.path.join(self.datasets_base, 'splits', self.splits_filename[0])) as f:
            data = json.loads(f.read())
            for i, split in enumerate(data):
                if i == self.split_index:
                    self.split = split
                    break

        for video_name in self.split[self.mode + '_keys']:
            video_name = os.path.basename(video_name)
            frame_features = torch.Tensor(np.array(hdf[video_name + '/features']))
            gtscore = torch.Tensor(np.array(hdf[video_name + '/gtscore']))

            self.list_frame_features.append(frame_features)
            self.list_gtscores.append(gtscore)

        hdf.close()

    def __len__(self):
        """ Function to be called for the `len` operator of `VideoData` Dataset. """
        self.len = len(self.split[self.mode + '_keys'])
        return self.len

    def __getitem__(self, index):
        """ Function to be called for the index operator of `VideoData` Dataset.
        train mode returns: frame_features and gtscores
        test mode returns: frame_features and video name

        :param int index: The above-mentioned id of the data.
        """
        video_name = self.split[self.mode + '_keys'][index]
        video_name = os.path.basename(video_name)
        frame_features = self.list_frame_features[index]
        gtscore = self.list_gtscores[index]

        if self.mode == 'test':
            return frame_features, video_name
        else:
            return frame_features, gtscore


def get_loader(mode, video_type, split_index):
    """ Loads the `data.Dataset` of the `split_index` split for the `video_type` Dataset.
    Wrapped by a Dataloader, shuffled and `batch_size` = 1 in train `mode`.

    :param str mode: The mode of the model, train or test.
    :param str video_type: The Dataset being used, SumMe or TVSum.
    :param int split_index: The index of the Dataset split being used.
    :return: The Dataset used in each mode.
    """
    if mode.lower() == 'train':
        vd = VideoData(mode, video_type, split_index)
        return DataLoader(vd, batch_size=1, shuffle=True)
    else:
        return VideoData(mode, video_type, split_index)
