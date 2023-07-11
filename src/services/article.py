"""
@Author: Ye Huang
"""
import re

from src.classes.model import DataModel
from src.resources.database import Tables

Article: DataModel = getattr(Tables, 'Articles')
article_logger = Article.logger
article_fields = getattr(Tables, 'ArticlesField')

Collect: DataModel = getattr(Tables, 'Collect')
collect_logger = Collect.logger
collect_fields = getattr(Tables, 'CollectField')

UserInfo: DataModel = getattr(Tables, 'Userinfo')
userinfo_fileds = getattr(Tables, 'Userinfo')
userinfo_logger = UserInfo.logger


def get_list(**kwargs):
    """
    获取资讯列表

    :param kwargs: 前端类别参数和用户id
    :return:result
    """
    result = Article.get_record(**article_fields(**kwargs).dict(exclude_none=True))
    if result is None:
        article_logger.error(f'无内容:{kwargs}')
        raise ValueError(f'无内容:{kwargs}')
    else:
        res = []
        info_dict = {'collector_id': kwargs.get('userid')}
        for row in result:
            temp = row.to_json()
            info_dict.update({"article_id": row.id})
            isCollect = Collect.get_record(**info_dict)
            if isCollect:
                temp.update(isCollected=1)
                res.append(temp)
            else:
                temp.update(isCollected=0)
                res.append(temp)
    return res


def get_detail(**kwargs):
    """
    获取资讯详情

    :param kwargs: 帖子id
    :return: result
    """
    result = Article.get_record(**article_fields(**kwargs).dict(exclude_none=True))
    if result is None:
        article_logger.error(f'无内容:{kwargs}')
        raise ValueError(f'无内容:{kwargs}')
    else:
        return result


def search(**kwargs):
    """
    获取资讯详情

    :param kwargs: 搜索关键字keyword和用户userid
    :return: result
    """
    result = Article.get_record(**article_fields(**kwargs).dict(exclude_none=True))
    if result is None:
        article_logger.error(f'无内容:{kwargs}')
        raise ValueError(f'无内容:{kwargs}')
    else:
        key = kwargs.get('keyword')
        info_dict = {'collector_id': kwargs.get('userid')}
        suggestions = []
        pattern = '.*%s.*' % key
        regex = re.compile(pattern)
        for item in result:
            temp = item.to_json()
            match = regex.search(temp['content'])
            if match:
                info_dict.update({"article_id": temp['id']})
                isCollect = Collect.get_record(**info_dict)
                if isCollect:
                    temp.update(isCollected=1)
                else:
                    temp.update(isCollected=0)
                suggestions.append(temp)
        return suggestions


def collect(**kwargs):
    """
    收藏资讯

    :param kwargs: collector_id,article_id
    :return: code
    """
    if Collect.add_record(**kwargs) is None:
        article_logger.error(f'收藏失败:{kwargs}')
        raise ValueError(f'收藏失败: {kwargs}')


def disCollect(**kwargs):
    """
    取消收藏

    :param kwargs: collector_id,article_id
    :return: code
    """
    if Collect.get_record(**kwargs) is None:
        article_logger.error(f'未收藏:{kwargs}')
        raise ValueError(f'未收藏:{kwargs}')
    else:
        res = Collect.get_record(**kwargs)
        id_dict = {"id": res[0].id}
        if Collect.delete_record(**id_dict) is False:
            article_logger.error(f'取消收藏失败:{kwargs}')
            raise ValueError(f'取消收藏失败: {kwargs}')


def add_article(**kwargs):
    """
    添加文章

    :param kwargs: title,content,create_time,author,picture,type,class_,userid
    :return: code
    """
    result = UserInfo.get_record(**{'openid': kwargs.get('id')})
    if len(result) == 0:
        article_logger.error(f'该用户不存在:{kwargs}')
        raise ValueError(f'该用户不存在:{kwargs}')
    else:
        user = result[0]
        user_type = user['type']
        if not user_type == 1:
            article_logger.error(f'该用户无权限:{kwargs}')
            raise ValueError(f'该用户无权限:{kwargs}')
    if Article.add_record(**kwargs) is None:
        article_logger.error(f'添加文章失败:{kwargs}')
        raise ValueError(f'添加文章失败:{kwargs}')


def delete_article(**kwargs):
    """
    删除文章

    :param kwargs: userid,article_id
    :return: code
    """
    id_dict = {"id": kwargs.get('article_id')}
    user_dict = {'openid': kwargs.get('id')}
    result = UserInfo.get_record(**user_dict)
    if len(result) == 0:
        article_logger.error(f'该用户不存在:{kwargs}')
        raise ValueError(f'该用户不存在:{kwargs}')
    else:
        user_type = result[0]['type']
        if not user_type == 1:
            article_logger.error(f'该用户无权限:{kwargs}')
            raise ValueError(f'该用户无权限:{kwargs}')
    if len(Article.get_record(**id_dict)) == 0:
        article_logger.error(f'该文章不存在:{kwargs}')
        raise ValueError(f'该文章不存在:{kwargs}')
    else:
        if not Article.delete_record(**id_dict):
            article_logger.error(f'删除文章失败:{kwargs}')
            raise ValueError(f'删除文章失败:{kwargs}')
