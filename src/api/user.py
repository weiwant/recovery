from typing import Optional

from pydantic import BaseModel, ValidationError
from sanic import Request, Blueprint

from src.classes.response import Response
from src.services.user import add_user, exist_user, get_user, update_user, delete_user,add_patient,add_doctor
from src.utils.logger import get_logger

user_blueprint = Blueprint('user', url_prefix='/user')
logger = get_logger(__name__)


@user_blueprint.route('/register', methods=['POST'])
async def register(request: Request):
    """
    用户注册

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
        type: int
        session_key: Optional[str]
        nickname: Optional[str]

    try:
        checked = Check(**data).dict(exclude_none=True)
        if exist_user(openid=checked['openid']):
            return Response(403, '用户已存在').text()
        if checked.get('nickname', None) is None:
            checked['nickname'] = '微信用户'
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
        type: int

        class Config:
            """
            配置
            """
            extra = 'allow'

    try:
        checked = Check(**data).dict(exclude_none=True)
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
        checked = Check(**data).dict(exclude_none=True)
        if checked['type']==2:
            add_patient(**checked)
        elif checked['type']==3:
            add_doctor(**checked)
        return Response(200, '添加成功').text()
    except ValidationError as e:
        logger.error(f'参数错误: {e}')
        return Response(400, '参数错误').text()
    except Exception as e:
        logger.error(f'添加用户信息失败: {e}')
        return Response(500, '添加用户信息失败').text()

