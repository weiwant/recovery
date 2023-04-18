from Crypto.Hash import MD5

from src.models.error import DataError, RuleError
from src.models.mapper import Mapper
from src.models.model import DataModel
from src.services import session_maker, base

fields = Mapper({
    'id': 'id',
    'username': 'username',
    'password': 'password',
    'type': 'type',
    'iv': 'iv',
    'login_host': 'loginhost'
})


class UserService:
    user_info = DataModel(__name__, base.classes['userinfo'], session_maker, fields.map_dict['id'])
    logger = user_info.logger

    @classmethod
    def check_exist(cls, **kwargs):
        """
        检查是否存在

        :param kwargs: dict
        :return: bool
        """
        username = kwargs.get(fields.map_dict['username'])
        result = cls.user_info.get_record(**{fields.map_dict['username']: username})
        if result is None:
            raise DataError('操作失败')
        return bool(result)

    @classmethod
    def add_user(cls, **kwargs):
        """
        添加用户

        :param kwargs: dict
        :return: int
        """
        if cls.check_exist(**kwargs):
            raise RuleError('用户名已存在')
        kwargs[fields.map_dict['password']] = MD5.new(kwargs[fields.map_dict['password']].encode()).hexdigest()
        result = cls.user_info.add_record(**kwargs)
        if result is None:
            raise DataError('操作失败')
        return result

    @classmethod
    def delete_user(cls, userid):
        """
        删除用户

        :param userid: int
        :return: bool
        """
        result = cls.user_info.delete_record(**{fields.map_dict['id']: userid})
        if not result:
            raise DataError('操作失败')
        return result
