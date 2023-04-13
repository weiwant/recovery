from logging import getLogger, StreamHandler, Formatter


def get_logger(name):
    logger = getLogger(name)
    logger.setLevel('INFO')
    console = StreamHandler()
    console.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console)
    return logger
