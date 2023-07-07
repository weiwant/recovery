import json
import os

import numpy


class dataloader:
    def __init__(self, data_path='datasets/correct', dataset='default'):
        """
        初始化

        :param data_path: 数据集路径
        :param dataset: 数据集名称
        """
        self.data_path = data_path
        self.split_path = os.path.join(data_path, 'split')
        self.dataset = dataset

    def get_data(self, mode='train'):
        """
        获取训练数据

        :return:
        """
        dataset = next(filter(lambda x: self.dataset in x, os.listdir(self.data_path)))
        split = next(filter(lambda x: self.dataset in x, os.listdir(self.split_path)))
        split = json.load(open(split, 'r'))
        dataset = json.load(open(dataset, 'r'))
        return [(numpy.array(dataset[i]['feature']), numpy.array(dataset[i]['template']),
                 numpy.array(dataset[i]['label']).astype(numpy.bool_)) for i in split[mode]]
