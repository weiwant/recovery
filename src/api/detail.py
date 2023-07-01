from datetime import date
from typing import List

from pydantic import BaseModel, ValidationError, validator
from sanic import Request, Blueprint

from src.classes.response import Response
from src.services.detail import add_detail, get_detail, upload_video, update_detail
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
        deadline: date

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
        result = get_task(id=data['task'])[0]
        data['deadline'] = getattr(result, 'deadline')
        checked = Check(**data).dict(exclude_none=True)
        checked['finish_date'] = date.today()
        exist = False
        result_detail = get_detail(**{'task': checked['task'], 'finish_date': checked['finish_date']})
        if result_detail:
            exist = True
        checked['score'], checked['evaluation'] = inference(checked['video'], getattr(result, 'training_root'),
                                                            getattr(result, 'evaluate_root'))
        if exist:
            checked.update({'id': getattr(result_detail[0], 'id')})
            update_detail(**checked)
        else:
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
        checked = Check(**data).dict(exclude_none=True)
        checked['video'] = request.files['video'][0]
        checked['video_type'] = checked['video_type'][0]
        checked['task'] = checked['task'][0]
        result = get_task(id=checked['task'])[0]
        checked['training_root'] = getattr(result, 'training_root')
        file_name = upload_video(**checked)
        return Response(200, data=file_name).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()