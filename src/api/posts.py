"""
@Author: Ye Huang
"""
import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ValidationError
from sanic import Blueprint, Request

from src.classes.response import Response
from src.services.posts import add_post, get_post_list, get_post_detail, like_post, comment_post, dislike_post, \
    delete_post
from src.utils.logger import get_logger

posts_blueprint = Blueprint("posts", url_prefix="/posts")
logger = get_logger(__name__)


@posts_blueprint.route('/add', methods=['POST'])
async def add(request: Request):
    """
    用户发帖

    :param request: 请求
    :return: 响应结果
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        content: str
        pictures: Optional[list]
        creator: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        checked['create_time'] = datetime.datetime.now()
        checked['views'] = 0
        checked['stars'] = 0
        checked['id'] = uuid.uuid4()
        add_post(**checked)
        return Response(200, '发布成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'添加失败: {e}')
        return Response(500, '添加失败').text()


@posts_blueprint.route("/get_list", methods=['POST'])
async def get_list(request: Request):
    """
    用户获取列表

    :param request: request
    :return: Response
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        userid: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        res = get_post_list(**checked)
        return Response(200, data=res).json()
    except ValueError:
        logger.error(f'无内容')
        return Response(403, '无内容').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()


@posts_blueprint.route("/get_detail", methods=['POST'])
async def get_tail(request: Request):
    """
    用户获取帖子详情

    :param request: request
    :return: 详情
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        userid: str
        id: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        res = get_post_detail(**checked)
        return Response(200, data=res).json()
    except ValueError:
        logger.error(f'无内容')
        return Response(403, '无内容').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()


@posts_blueprint.route("/like", methods=['POST'])
async def like(request: Request):
    """
    用户点赞帖子

    :param request: request
    :return: 响应结果
    """

    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        userid: str
        post_id: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        like_post(**checked)
        return Response(200, message='点赞成功').text()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'点赞失败：{e}')
        return Response(500, "点赞失败").text()


@posts_blueprint.route('/dislike', methods=['POST'])
async def dislike(request: Request):
    """
    用户取消点赞帖子

    :param request: request
    :return: response
    """

    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        userid: str
        post_id: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        dislike_post(**checked)
        return Response(200, message='取消点赞成功').text()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'取消点赞失败：{e}')
        return Response(500, "取消点赞失败").text()


@posts_blueprint.route('/comment', methods=['POST'])
async def comment(request: Request):
    """
    用户评论

    :param request: request
    :return: 响应结果
    """

    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        commenter: str
        post_id: str
        content: str
        parent: Optional[str]

    try:
        checked = Check(**data).dict(exclude_none=True)
        checked['id'] = uuid.uuid4()
        comment_post(**checked)
        return Response(200, message='评论成功').text()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'评论失败：{e}')
        return Response(500, "评论失败").text()


@posts_blueprint.route('/delete', methods=['POST'])
async def delete(request: Request):
    """
    删除帖子

    :param request: request
    :return: 响应结果
    """

    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        userid: str
        post_id: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        delete_post(**checked)
        return Response(200, message='删除成功').text()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'评论失败：{e}')
        return Response(500, "删除失败").text()
