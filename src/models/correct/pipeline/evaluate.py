"""
@Author: Wenfeng Zhou
"""
import os.path

import joblib
import numpy

from src.models.correct.algorithm.model import Correct
from src.models.correct.utils.config import get_config
from src.models.correct.utils.data import dataloader


def main(args):
    model = Correct(**joblib.load(os.path.join(args['model_path'], 'correct.pkl')))
    for (feature, template, label) in dataloader().get_data('test'):
        _, _, e = model.run(feature, template)
        print(format(numpy.sum(e < model.k & label) / numpy.sum(label), '.2%'))


if __name__ == '__main__':
    config = get_config('test')
    main(config)
