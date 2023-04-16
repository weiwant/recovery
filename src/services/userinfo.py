from src.models.mapper import Mapper
from src.models.model import DataModel
from src.services import session_maker, base

user_info = DataModel(__name__, base.classes['userinfo'], session_maker, 'id')
logger = user_info.logger
fields = Mapper({
    'id': 'id',
    'username': 'username',
    'password': 'password',
    'type': 'type'
})


def register(**kwargs):
    """
    注册

    :param kwargs:
    :return:
    """
    if fields.has_values(kwargs, ['username', 'password', 'type']):
        result = user_info.add_record(**kwargs)
        return 200 if result is not None else 500, result
    else:
        logger.error('缺少参数')
        return 500, None


def login(**kwargs):
    """
    登录

    :param kwargs:
    :return:
    """
    if fields.has_values(kwargs, ['username', 'password']):
        result = user_info.get_record(**kwargs)
        if result is None:
            return 500, None
        elif not result:
            return 401, None
        else:
            return 200, result
    else:
        logger.error('缺少参数')
        return 500, None
