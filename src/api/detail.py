"""
@Author: Wenfeng Zhou
"""
import datetime
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
        data['deadline'] = result['deadline']
        checked = Check(**data).dict(exclude_none=True)
        checked['finish_date'] = str(datetime.datetime.now())
        exist = False
        result_detail = get_detail(**{'task': checked['task'], 'finish_date': checked['finish_date']})
        if result_detail:
            exist = True
        checked['score'], checked['evaluation'] = inference(checked['video'], result['training_root'],
                                                            result['evaluate_root'], result['type'])
        if exist:
            checked.update({'id': getattr(result_detail[0], 'id')})
            update_detail(**checked)
        else:
            add_detail(**checked)
        return Response(200,
                        data={'score': format(checked['score'] * 100, '.2f'),
                              'evaluation': checked['evaluation']}).json()
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

    try:
        checked = Check(**data).dict(exclude_none=True)
        result = get_detail(**checked)
        result = [i.to_json() for i in result]
        for r in result:
            date_string, time_string = str(r['finish_date']).split(' ')
            r['date'] = date_string[5:]
            r['time'] = time_string[:8]
            r['isMorn'] = int(time_string <= '12:00:00')
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
        checked['training_root'] = result['training_root']
        file_name = upload_video(**checked)
        return Response(200, message=file_name).text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()


@detail_blueprint.route('/lines', methods=['POST'])
async def lines(request: Request):
    """
    获取折线图数据

    :param request:
    :return:
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        openid: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        tasks = get_task(patient=checked['openid'])
        results = []
        for task in tasks:
            temp = {
                'type': 'line',
                'smooth': True,
                'data': [],
                'name': task['type']
            }
            details = get_detail(task=task['id'])
            for detail in details:
                temp['data'].append(detail.score)
            results.append(temp)
        return Response(200, data=results).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()
