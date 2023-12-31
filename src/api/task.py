"""
@Author: Wenfeng Zhou, Ye Huang
"""
import json
from datetime import date, datetime
from enum import IntEnum
from typing import Optional

from Crypto.Hash import SHA256
from pydantic import BaseModel, ValidationError, validator
from sanic import Request, Blueprint

from src.classes.response import Response
from src.services.detail import get_detail
from src.services.task import add_task, get_task, update_task, delete_task, get_task_info
from src.utils.logger import get_logger

task_blueprint = Blueprint('task', url_prefix='/task')
logger = get_logger(__name__)


@task_blueprint.route('/add', methods=['POST'])
async def add(request: Request):
    """
    添加任务

    :author: Wenfeng Zhou
    :param request: 请求
    :return:
    """
    await request.receive_body()
    data = request.json

    class DifficultyValue(IntEnum):
        """
        难度枚举
        """
        EASY = 0
        MIDDLE = 1
        HARD = 2

    class Check(BaseModel):
        """
        检查数据
        """
        description: str
        deadline: date
        doctor: str
        patient: str
        circle_time: str
        type: str
        difficulty: DifficultyValue

        @classmethod
        @validator('deadline', allow_reuse=True)
        def deadline_must_greater_than_today(cls, v):
            """
            截止日期必须大于今天
            :param v:
            :return:
            """
            if v < date.today():
                raise ValueError('截止日期必须大于今天')
            return v

    try:
        checked = Check(**data).dict(exclude_none=True)
        checked['status'] = 0
        checked['create_time'] = date.today()
        checked['training_root'] = SHA256.new((str(datetime.now()) + json.dumps(data)).encode()).hexdigest()
        checked['evaluate_root'] = SHA256.new((str(datetime.now()) + json.dumps(data)).encode()).hexdigest()
        checked['difficulty'] = int(checked['difficulty'])
        add_task(**checked)
        return Response(200, '添加成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'添加失败: {e}')
        return Response(500, '添加失败').text()


@task_blueprint.route('/delete', methods=['POST'])
async def delete(request: Request):
    """
    删除任务

    :author: Wenfeng Zhou
    :param request:
    :return:
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        id: int

    try:
        checked = Check(**data).dict(exclude_none=True)
        temp = get_task(id=checked['id'])[0]
        checked['training_root'] = temp['training_root']
        checked['evaluate_root'] = temp['evaluate_root']
        delete_task(**checked)
        return Response(200, '删除成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'删除失败: {e}')
        return Response(500, '删除失败').text()


@task_blueprint.route('/update', methods=['POST'])
async def update(request: Request):
    """
    更新任务

    :author: Wenfeng Zhou
    :param request: 请求
    :return:
    """
    await request.receive_body()
    data = request.json

    class DifficultyValue(IntEnum):
        """
        难度枚举
        """
        EASY = 0
        MIDDLE = 1
        HARD = 2

    class State(IntEnum):
        """
        状态枚举
        """
        UNDO = 0
        DOING = 1
        DONE = 2

    class Check(BaseModel):
        """
        检查数据
        """
        id: int
        status: Optional[State]
        description: Optional[str]
        deadline: Optional[date]
        circle_time: Optional[str]
        type: Optional[str]
        difficulty: Optional[DifficultyValue]

        @classmethod
        @validator('deadline', allow_reuse=True)
        def deadline_must_greater_than_today(cls, v):
            """
            截止日期必须大于今天

            :param v:
            :return:
            """
            if v and v < date.today():
                raise ValueError('截止日期必须大于今天')
            return v

    try:
        checked = Check(**data).dict(exclude_none=True)
        if checked.get('difficulty', None) is not None:
            checked['difficulty'] = int(checked['difficulty'])
        if checked.get('status', None) is not None:
            checked['status'] = int(checked['status'])
        update_task(**checked)
        return Response(200, '更新成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'更新失败: {e}')
        return Response(500, '更新失败').text()


@task_blueprint.route('/get', methods=['POST'])
async def get(request: Request):
    """
    获取任务

    :author: Wenfeng Zhou
    :param request:
    :return:任务列表
    """
    await request.receive_body()
    data = request.json

    try:
        result = get_task(**data)
        return Response(200, data=result).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()


@task_blueprint.route('/get_info', methods=['POST'])
async def get_info(request: Request):
    """
    获取任务详细信息

    :author: Ye Huang
    :param request:
    :return:
    """

    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        id: int

    try:
        checked = Check(**data).dict(exclude_none=True)
        res = get_task_info(**checked)
        return Response(200, data=res).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()


@task_blueprint.route('/date_list', methods=['POST'])
async def date_list(request: Request):
    """
    获取任务日期列表

    :author: Wenfeng Zhou
    :param request: 请求
    :return: 任务日期列表
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        id: int

    try:
        checked = Check(**data).dict(exclude_none=True)
        result = get_detail(**{'task': checked['id']})
        results = []
        for r in result:
            dt = getattr(r, 'finish_date')
            results.append(str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day))
        return Response(200, data=results).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()
