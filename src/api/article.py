"""
@Author: Ye Huang
"""
from typing import Optional

from pydantic import BaseModel, ValidationError
from sanic import Blueprint, Request

from src.classes.response import Response
from src.services.article import get_list, get_detail, search, collect, disCollect, add_article, delete_article
from src.utils.logger import get_logger

article_blueprint = Blueprint('article', url_prefix='/article')
logger = get_logger(__name__)


@article_blueprint.route("/get_list", methods=['POST'])
async def get1(request: Request):
    """
    获取资讯列表

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
        class_: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        res = get_list(**checked)
        return Response(200, data=res).json()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'获取失败：{e}')
        return Response(500, "获取失败").text()


@article_blueprint.route("/get_detail", methods=['POST'])
async def get2(request: Request):
    """
    获取资讯详情

    :param request: request
    :return: 详情数据
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检测数据
        """
        id: int

    try:
        checked = Check(**data).dict(exclude_none=True)
        res = get_detail(**checked)
        return Response(200, data=res).json()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'获取失败：{e}')
        return Response(500, "获取失败").text()


@article_blueprint.route("/search", methods=['POST'])
async def search1(request: Request):
    """
    关键字搜索帖子

    :param request: request
    :return: 对应帖子列表
    """

    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        keyword: str
        userid: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        res = search(**checked)
        if not res:
            return Response(200, message="无匹配结果").text()
        else:
            return Response(200, data=res).json()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'获取失败：{e}')
        return Response(500, "获取失败").text()


@article_blueprint.route("/collect", methods=['POST'])
async def collect1(request: Request):
    """
    收藏资讯

    :param request: request
    :return: 状态
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        article_id: str
        collector_id: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        collect(**checked)
        return Response(200, "收藏成功").text()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'获取失败：{e}')
        return Response(500, "收藏失败").text()


@article_blueprint.route("/discollect", methods=['POST'])
async def discollect1(request: Request):
    """
    取消收藏资讯

    :param request: request
    :return: 状态
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        article_id: str
        collector_id: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        disCollect(**checked)
        return Response(200, "取消收藏成功").text()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'获取失败：{e}')
        return Response(500, "收藏失败").text()


@article_blueprint.route('/add', methods=['POST'])
async def add(request: Request):
    """
    发布新文章

    :param request: request
    :return: 状态
    """

    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        userid: str
        title: str
        author: str
        content: str
        url: Optional[str]
        type: int
        class_: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        add_article(**checked)
        return Response(200, "添加成功").text()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'添加失败：{e}')
        return Response(500, "添加失败").text()


@article_blueprint.route('delete', methods=['POST'])
async def delete(request: Request):
    """
    删除文章

    :param request: request
    :return: 状态
    """

    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
         检测数据
        """
        userid: str
        article_id: int

    try:
        checked = Check(**data).dict(exclude_none=True)
        delete_article(**checked)
        return Response(200, "删除成功").text()
    except ValidationError as e:
        logger.error(f'参数错误:{e}')
        return Response(400, "参数错误").text()
    except Exception as e:
        logger.error(f'删除失败：{e}')
        return Response(500, "删除失败").text()
