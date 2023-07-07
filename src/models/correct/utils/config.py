import argparse


def get_config(mode='train'):
    """
    获取配置

    :param mode: 模式
    :return:
    """
    parser = argparse.ArgumentParser()
    if mode == 'train':
        parser.add_argument('--step', type=float, default=0.1, help='number of steps')
        parser.add_argument('--save-path', type=str, default='models/correct', help='path to save processed data')
        kwargs = vars(parser.parse_args())
    elif mode == 'test':
        parser.add_argument('--model-path', type=str, default='models/correct', help='path to save processed data')
        kwargs = vars(parser.parse_args())
    else:
        raise ValueError('mode must be train or test')
    return kwargs
