"""
@Author: Ye Huang
"""
import datetime

from src.classes.model import DataModel
from src.resources.database import Tables

Posts: DataModel = getattr(Tables, 'Posts')
posts_logger = Posts.logger
posts_fields = getattr(Tables, 'PostsField')

Userinfo: DataModel = getattr(Tables, 'Userinfo')
user_logger = Userinfo.logger
user_fields = getattr(Tables, 'UserinfoField')
Likes: DataModel = getattr(Tables, 'Likes')
likes_logger = Likes.logger
Comment: DataModel = getattr(Tables, 'Comments')
comment_logger = Comment.logger


def add_post(**kwargs):
    """
    新发布帖子

    :param kwargs: creator，content
    :return: code
    """

    if Posts.add_record(**kwargs) is None:
        posts_logger.error(f'添加失败:{kwargs}')
        raise ValueError(f'添加任务失败: {kwargs}')


def get_post_list(**kwargs):
    """
    查询每个帖子的创建者名称、头像、type。查询该用户点赞状态“isGood”，以及每个帖子的评论数，返回json列表

    :param kwargs: 用户id
    :return: 列表数据
    """
    result = Posts.get_record(**posts_fields(**kwargs).dict(exclude_none=True))
    if result is None:
        posts_logger.error(f'内容为空:{kwargs}')
        raise ValueError(f'内容为空:{kwargs}')
    else:
        reslist = []
        for item in result:
            temp = item.to_json()
            user1 = Userinfo.get_record(**{"openid": temp['creator']})
            user = user1[0].to_json() if user1 else None
            if user1 is None:
                posts_logger.error(f'无此用户:{kwargs}')
                raise ValueError(f'无此用户:{kwargs}')
            else:
                temp.update(username=user['nickname'])
                temp.update(userImag=user['img'])
                usr_type = user['type']
                if usr_type == 3:
                    temp.update(isDoctor=1)
                else:
                    temp.update(isDoctor=0)
                kwargs.update(post_id=temp['id'])
                res1 = Likes.get_record(**kwargs)
                if len(res1) == 0:
                    temp.update(isGood=0)
                else:
                    temp.update(isGood=1)
                post_dict = {'post_id': temp['id']}
                res2 = Comment.get_record(**post_dict)
                count = len(res2)
                temp.update(comment=count)
                res3 = Likes.get_record(**post_dict)
                count1 = len(res3)
                temp.update(good=count1)
                reslist.append(temp)
        return reslist


def get_post_detail(**kwargs):
    """
    查看帖子详情

    :param kwargs: 帖子id和用户id
    :return: 帖子详情+评论列表详情

    """
    dict2 = {'post_id': kwargs['id']}
    res = Posts.get_record(**posts_fields(**kwargs).dict(exclude_none=True))
    if res is None:
        posts_logger.error(f'此帖不存在:{kwargs}')
        raise ValueError(f'此帖不存在:{kwargs}')
    else:
        temp = res[0].to_json()
        user1 = Userinfo.get_record(**{'openid': temp['creator']})
        user = user1[0].to_json()
        if user1 is None:
            posts_logger.error(f'无此用户:{kwargs}')
            raise ValueError(f'无此用户:{kwargs}')
        else:
            temp.update(username=user['nickname'])
            temp.update(userImag=user['img'])
            usr_type = user['type']
            if usr_type == 3:
                temp.update(isDoctor=1)
            else:
                temp.update(isDoctor=0)
        info_dict = {'post_id': kwargs['id'], 'userid': kwargs['userid']}
        res1 = Likes.get_record(**info_dict)
        if len(res1) == 0:
            temp.update(isGood=0)
        else:
            temp.update(isGood=1)
        res3 = Likes.get_record(**dict2)
        count1 = len(res3)
        temp.update(good=count1)
        res2 = Comment.get_record(**dict2)
        res2 = sorted(res2, key=lambda x: x.comment_time)  # 排序
        count = len(res2)
        temp.update(comment=count)
        if not count == 0:
            final_list = []
            comment_list = {}  # 最后返回的评论
            for item in res2:
                openid = {'openid': item.commenter}
                user = Userinfo.get_record(**openid)
                user1 = user[0].to_json()
                json_dict = item.to_json()
                if not json_dict['parent'] is None:  # 是子级评论，添加到父级的子评论列表中
                    add = {'username': user1['nickname'], 'cont': json_dict['content']}  # 子评论添加的用户名和内容
                    comment_list[json_dict['parent']]['children'].append(add)
                else:  # 不是子评论,查找用户头像+返回数据
                    add2 = {'username': user1['nickname'], 'userUrl': user1['img'], 'children': []}
                    json_dict.update(add2)
                    comment_list.update({json_dict['id']: json_dict})
            for i in comment_list.keys():
                final_list.append(comment_list[i])
            temp.update({'comment': final_list})
        view = res[0].views
        view_dict = {'id': kwargs['id']}
        view_dict.update({'views': view + 1})
        if not Posts.update_record(**view_dict):
            posts_logger.error(f'更新浏览量失败: {kwargs}')
            raise ValueError(f'更新浏览量失败: {kwargs}')
        else:
            temp.update(view_dict)
    return temp


def like_post(**kwargs):
    """
    点赞帖子

    :param kwargs: 用户id和帖子id
    :return:
    """
    pre = Likes.get_record(**kwargs)
    if not len(pre) == 0:
        posts_logger.error(f"已点赞:{kwargs}")
        raise ValueError(f'已点赞:{kwargs}')
    else:
        id_dict = {'id': kwargs.get('post_id')}
        res = Posts.get_record(**id_dict)
        star = res[0].stars
        id_dict.update({'stars': star + 1})
        if not Posts.update_record(**id_dict):
            posts_logger.error(f'更新记录失败: {kwargs}')
            raise ValueError(f'更新记录失败: {kwargs}')
        else:
            Likes.add_record(**kwargs)


def comment_post(**kwargs):
    """
    帖子评论
    todo:子评论处理

    :param kwargs: 用户id，帖子id，评论内容，是否子评论，父评论id
    :return: 状态码
    """
    if kwargs.get('parent') is None:
        kwargs.update({'comment_time': datetime.datetime.now()})
        if Comment.add_record(**kwargs) is None:
            comment_logger.error(f'评论失败: {kwargs}')
            raise ValueError(f'评论失败: {kwargs}')


def dislike_post(**kwargs):
    """
    取消点赞帖子

    :param kwargs: 用户id和帖子id
    :return:
    """
    pre = Likes.get_record(**kwargs)
    if len(pre) == 0:
        posts_logger.error(f"未点赞:{kwargs}")
        raise ValueError(f'未点赞:{kwargs}')
    else:
        id_dict = {'id': kwargs.get('post_id')}
        res = Posts.get_record(**id_dict)
        star = res[0].stars
        id_dict.update({'stars': star - 1})
        if not Posts.update_record(**id_dict):
            posts_logger.error(f'更新记录失败: {kwargs}')
            raise ValueError(f'更新记录失败: {kwargs}')
        else:
            res = Likes.get_record(**kwargs)
            id_dict = {'id': res[0].id}
            if Likes.delete_record(**id_dict) is False:
                posts_logger.error(f'取消点赞失败:{kwargs}')
                raise ValueError(f'取消点赞失败:{kwargs}')


def delete_post(**kwargs):
    """
    删除帖子

    :param kwargs: 用户id和帖子id
    :return:
    """
    post_dict = {'id': kwargs.get('post_id')}
    if len(Posts.get_record(**post_dict)) == 0:
        posts_logger.error(f'无此内容:{kwargs}')
        raise ValueError(f'无此内容:{kwargs}')
    else:
        author = Posts.get_record(**post_dict)[0]['creator']
        if not author == kwargs.get('userid'):
            posts_logger.error(f'无权限:{kwargs}')
            raise ValueError(f'无权限:{kwargs}')
        else:
            if not Posts.delete_record(**post_dict):
                posts_logger.error(f'删除失败:{kwargs}')
                raise ValueError(f'删除失败:{kwargs}')
