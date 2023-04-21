import json
import os
import shutil
from datetime import date
from datetime import datetime
from enum import IntEnum

from Crypto.Hash import SHA256
from pydantic import BaseModel, ValidationError, validator
from sanic import Request, Blueprint

from src.classes.response import Response
from src.services.task import add_task, get_task, update_task, delete_task
from src.utils.logger import get_logger

task_blueprint = Blueprint('task', url_prefix='/task')
logger = get_logger(__name__)


@task_blueprint.route('/add', methods=['POST'])
async def add(request: Request):
    """
    添加任务

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

        @validator('deadline')
        def deadline_must_greater_than_today(self, v):
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
        if not os.path.exists(f'./training/{checked["training_root"]}'):
            os.makedirs(f'./training/{checked["training_root"]}')
        if not os.path.exists(f'./evaluation/{checked["evaluate_root"]}'):
            os.makedirs(f'./evaluation/{checked["evaluate_root"]}')
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
        temp = get_task(id=checked['id'])[0].to_json()
        training_root = temp['training_root']
        evaluate_root = temp['evaluate_root']
        delete_task(**checked)
        if os.path.exists(f'./training/{training_root}'):
            shutil.rmtree(f'./training/{training_root}')
        if os.path.exists(f'./evaluation/{evaluate_root}'):
            shutil.rmtree(f'./evaluation/{evaluate_root}')
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
        status: State
        description: str
        deadline: date
        circle_time: str
        type: str
        difficulty: DifficultyValue

        @validator('deadline')
        def deadline_must_greater_than_today(self, v):
            """
            截止日期必须大于今天

            :param v:
            :return:
            """
            if v < date.today():
                raise ValueError('截止日期必须大于今天')
            return v

        class Config:
            extra = 'ignore'

    try:
        checked = Check(**data).dict(exclude_none=True)
        checked['difficulty'] = int(checked['difficulty'])
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

    :param request: 请求
    :return:
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        id: int

        class Config:
            extra = 'allow'

    try:
        checked = Check(**data).dict(exclude_none=True)
        result = get_task(**checked)
        return Response(200, data=result).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()
