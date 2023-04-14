from logging import getLogger, StreamHandler, Formatter


def get_logger(name):
    """
    获取日志记录器

    :param name: 日志记录器名称
    :return: 日志记录器
    """
    logger = getLogger(name)
    logger.setLevel('INFO')
    console = StreamHandler()
    console.setFormatter(Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console)
    return logger
