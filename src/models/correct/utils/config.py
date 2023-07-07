import argparse


def get_config():
    """
    获取配置

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--iter', type=int, default=10, help='number of iterations')
    parser.add_argument('--step', type=float, default=0.1, help='number of steps')
    parser.add_argument('--save-path', type=str, default='models/correct', help='path to save processed data')
    kwargs = vars(parser.parse_args())
    return kwargs
