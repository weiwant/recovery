import os.path

import joblib
import numpy

from src.models.correct.algorithm.model import Correct
from src.models.correct.utils.config import get_config
from src.models.correct.utils.data import dataloader


def main(args):
    model = Correct()
    step = args['step']
    es = numpy.array([])
    labels = numpy.array([])
    for (feature, template, label) in dataloader().get_data():
        _, _, e = model.run(feature, template)
        es = numpy.concatenate((es, e))
        labels = numpy.concatenate((labels, label))
    f = numpy.frompyfunc(lambda k: 2 * numpy.sum(es < k & labels) / (
            2 * numpy.sum(es < k & labels) + numpy.sum(es < k & ~labels) + numpy.sum(es >= k & labels)), 1, 1)
    ks = numpy.arange(0, numpy.max(es), step)
    f1 = f(ks)
    best = numpy.argmax(f1)
    model.k = ks[best]
    joblib.dump({'k': model.k}, os.path.join(args['save_path'], 'correct.pkl'))


if __name__ == '__main__':
    config = get_config()
    main(config)
