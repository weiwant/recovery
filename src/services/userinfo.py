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
    args = ['username', 'password', 'type']
    if fields.has_values(kwargs, args):
        keys = [fields.map_dict[arg] for arg in args]
        values = [kwargs[key] for key in keys]
        result = user_info.add_record(**dict.fromkeys(keys, values))
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
    args = ['username', 'password']
    if fields.has_values(kwargs, args):
        keys = [fields.map_dict[arg] for arg in args]
        values = [kwargs[key] for key in keys]
        result = user_info.get_record(**dict.fromkeys(keys, values))
        if result is None:
            return 500, None
        elif not result:
            return 401, None
        else:
            return 200, result[0].to_json()
    else:
        logger.error('缺少参数')
        return 500, None
