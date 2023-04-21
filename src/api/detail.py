import os
from datetime import date
from typing import List
from uuid import uuid4

from pydantic import BaseModel, ValidationError
from sanic import Request, Blueprint

from src.classes.response import Response
from src.services.detail import add_detail, get_detail
from src.services.model import inference
from src.services.task import get_task
from src.utils.logger import get_logger

detail_blueprint = Blueprint('detail', url_prefix='/detail')
logger = get_logger(__name__)


@detail_blueprint.route('/add', methods=['POST'])
async def add(request: Request):
    """
    添加详情

    :param request: 请求
    :return:
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        task: int
        video: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        checked['finish_date'] = date.today()
        result = get_task(id=checked['task'])[0]
        checked['deadline'] = getattr(result, 'deadline')
        checked['score'], checked['evaluation'] = inference(checked['video'], getattr(result, 'training_root'),
                                                            getattr(result, 'evaluate_root'))
        add_detail(**checked)
        return Response(200, '添加成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'添加失败: {e}')
        return Response(500, '添加失败').text()


@detail_blueprint.route('/get', methods=['POST'])
async def get(request: Request):
    """
    获取详情

    :param request:
    :return:
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        task: int
        finish_date: date

    try:
        checked = Check(**data).dict(exclude_none=True)
        result = get_detail(**checked)[0].to_json()
        return Response(200, data=result).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()


@detail_blueprint.route('/upload', methods=['POST'])
async def upload(request: Request):
    """
    上传详情

    :param request:
    :return:
    """
    await request.receive_body()
    data = request.form

    class Check(BaseModel):
        """
        检查数据
        """
        task: List[int]
        video_type: List[str]

    try:
        file = request.files['video'][0]
        file_name = uuid4().hex
        checked = Check(**data).dict(exclude_none=True)
        file_name = file_name + '.' + checked['video_type'][0]
        result = get_task(id=checked['task'][0])[0]
        training_root = getattr(result, 'training_root')
        file_path = os.path.join('training', training_root, file_name)
        with open(file_path, 'wb') as f:
            f.write(file.body)
        return Response(200, data=file_name).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()
