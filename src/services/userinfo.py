from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.services import session_maker, base
from src.utils.logger import get_logger

logger = get_logger(__name__)
UserInfo = base.classes['userinfo']


def add_userinfo(username: str, password: str, usertype: int = 0):
    """
    添加用户信息

    :param username: 用户名
    :param password: 密码
    :param usertype: 用户类型
    :return:
    """
    with session_maker() as session:
        try:
            session: Session
            userinfo = UserInfo(username=username, password=password, type=usertype)
            session.add(userinfo)
            session.commit()
            return userinfo.id
        except IntegrityError as e:
            logger.error(f'添加用户信息失败: {e}')
            return None


def delete_userinfo(user_id: int):
    """
    删除用户信息

    :param user_id: 用户ID
    :return:
    """
    with session_maker() as session:
        session: Session
        session.query(UserInfo).filter(UserInfo.id == user_id).delete()
        session.commit()


def update_userinfo(user_id: int, username: str = None, password: str = None, usertype: int = None):
    """
    更新用户信息

    :param user_id: 用户ID
    :param username: 用户名
    :param password: 密码
    :param usertype: 用户类型
    :return:
    """
    with session_maker() as session:
        session: Session
        session.query(UserInfo).filter(UserInfo.id == user_id).update({
            UserInfo.username: username,
            UserInfo.password: password,
            UserInfo.type: usertype
        })
        session.commit()


def search_userinfo(user_id: int = None, username: str = None, password: str = None, usertype: int = None):
    """
    查询用户信息

    :param user_id: 用户ID
    :param username: 用户名
    :param password: 密码
    :param usertype: 用户类型
    :return:
    """
    with session_maker() as session:
        session: Session
        query = session.query(UserInfo)
        if user_id is not None:
            query = query.filter(UserInfo.id == user_id)
        if username is not None:
            query = query.filter(UserInfo.username == username)
        if password is not None:
            query = query.filter(UserInfo.password == password)
        if usertype is not None:
            query = query.filter(UserInfo.type == usertype)
        return query.all()
