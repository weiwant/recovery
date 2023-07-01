# -*- coding: utf-8 -*-
from src.models.keyframe.utils.config import get_config
from src.models.keyframe.utils.data import get_loader
from src.models.keyframe.utils.solver import Solver

if __name__ == '__main__':
    """ Main function that sets the data loaders; trains and evaluates the model."""
    config = get_config(mode='train')
    test_config = get_config(mode='test')

    print(config)
    print(test_config)
    print('Currently selected split_index:', config.split_index)
    train_loader = get_loader(config.mode, config.video_type, config.split_index)
    test_loader = get_loader(test_config.mode, test_config.video_type, test_config.split_index)
    solver = Solver(config, train_loader, test_loader)

    solver.build()
    solver.evaluate(-1)  # evaluates the summaries using the initial random weights of the network
    solver.train()
# tensorboard --logdir '../PGL-SUM/Summaries/PGL-SUM/'
