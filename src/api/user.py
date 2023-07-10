"""
@Author: Wenfeng Zhou, Ye Huang
"""
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel, ValidationError
from sanic import Request, Blueprint

from src.classes.response import Response
from src.services.task import delete_task, get_task
from src.services.user import add_user, exist_user, get_user, update_user, delete_user, add_patient, add_doctor, \
    bind_user, get_doctor, get_patient
from src.utils.logger import get_logger

user_blueprint = Blueprint('user', url_prefix='/user')
logger = get_logger(__name__)


@user_blueprint.route('/register', methods=['POST'])
async def register(request: Request):
    """
    用户注册

    :author: Wenfeng Zhou
    :param request: 请求
    :return:
    """
    await request.receive_body()
    data = request.json

    class TypeValue(IntEnum):
        """
        类型枚举
        """
        UNSET = 0
        ADMIN = 1
        PATIENT = 2
        DOCTOR = 3

    class Check(BaseModel):
        """
        检查数据
        """
        openid: str
        type: TypeValue
        session_key: Optional[str]
        nickname: Optional[str]

    try:
        checked = Check(**data).dict(exclude_none=True)
        if checked.get('nickname', None) is None:
            checked['nickname'] = '微信用户'
        checked['type'] = int(checked['type'])
        if exist_user(openid=checked['openid']):
            return Response(403, '用户已存在').text()
        add_user(**checked)
        return Response(200, '用户注册成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'用户注册失败: {e}')
        return Response(500, '用户注册失败').text()


@user_blueprint.route('/login', methods=['POST'])
async def login(request: Request):
    """
    用户登录

    :author: Wenfeng Zhou
    :param request: 请求
    :return:
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        openid: str
        session_key: Optional[str]

    try:
        checked = Check(**data).dict(exclude_none=True)
        if not exist_user(openid=checked['openid']):
            return Response(403, '用户不存在').text()
        data = get_user(**checked)
        return Response(200, data=data).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'用户登录失败: {e}')
        return Response(500, '用户登录失败').text()


@user_blueprint.route('/update', methods=['POST'])
async def update(request: Request):
    """
    更新用户信息

    :author: Wenfeng Zhou
    :param request:
    :return:
    """
    await request.receive_body()
    data = request.json

    class TypeValue(IntEnum):
        """
        类型枚举
        """
        UNSET = 0
        ADMIN = 1
        PATIENT = 2
        DOCTOR = 3

    class Check(BaseModel):
        """
        检查数据
        """
        openid: str
        type: TypeValue

        class Config:
            """
            配置
            """
            extra = 'allow'

    try:
        checked = Check(**data).dict(exclude_none=True)
        checked['type'] = int(checked['type'])
        update_user(**checked)
        return Response(200, '更新成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'更新用户信息失败: {e}')
        return Response(500, '更新用户信息失败').text()


@user_blueprint.route('/delete', methods=['POST'])
async def delete(request: Request):
    """
    删除用户

    :author: Wenfeng Zhou
    :param request: 请求
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
        result = get_user(**checked)
        user_type = result['type']
        temp = {}
        if user_type == 2:
            temp.update({'patient': checked['openid']})
        elif user_type == 3:
            temp.update({'doctor': checked['openid']})
        for task in get_task(**temp):
            delete_task(**{'id': getattr(task, 'id'), 'training_root': getattr(task, 'training_root'),
                           'evaluate_root': getattr(task, 'evaluate_root')})
        delete_user(**checked)
        return Response(200, '删除成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'删除用户失败: {e}')
        return Response(500, '删除用户失败').text()


@user_blueprint.route('/add-info', methods=['POST'])
async def add_info(request: Request):
    """
    添加用户信息

    :author: Wenfeng Zhou
    :param request: 请求
    :return:
    """
    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        userid: str
        type: int

        class Config:
            """
            配置
            """
            extra = 'allow'

    try:
        checked = Check(**data).dict(exclude_none=True, exclude={'type'})
        if data['type'] == 2:
            add_patient(**checked)
        elif data['type'] == 3:
            add_doctor(**checked)
        return Response(200, '添加成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'添加用户信息失败: {e}')
        return Response(500, '添加用户信息失败').text()


@user_blueprint.route('/bind', methods=['POST'])
async def bind1(request: Request):
    """
    添加医患绑定

    :author: Ye Huang
    :param request:
    :return: 响应状态
    """

    await request.receive_body()
    data = request.json

    class Check(BaseModel):
        """
        检查数据
        """
        patient: str
        doctor: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        bind_user(**checked)
        return Response(200, message='绑定成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'绑定失败: {e}')
        return Response(500, '绑定失败').text()


@user_blueprint.route('/doctor_list', methods=['POST'])
async def get_doctor1(request: Request):
    """
    患者获取医生列表

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
        patient: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        res = get_doctor(**checked)
        return Response(200, data=res).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()


@user_blueprint.route('/patient_list', methods=['POST'])
async def get_patient1(request: Request):
    """
    获取医生的患者列表

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
        doctor: str

    try:
        checked = Check(**data).dict(exclude_none=True)
        res = get_patient(**checked)
        return Response(200, data=res).json()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'获取失败: {e}')
        return Response(500, '获取失败').text()
