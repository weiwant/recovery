from sanic import Request, Blueprint

import src.services.userinfo
from src.models.response import Response

user_blueprint = Blueprint('user', url_prefix='/user')


@user_blueprint.route('/register', methods=['POST'])
async def register(request: Request):
    """
    注册

    :param request:
    :return:
    """
    await request.receive_body()
    status = src.services.userinfo.register(**request.json)[0]
    return Response(status_code=status, message='注册成功' if status == 200 else '注册失败').text()


@user_blueprint.route('/login', methods=['POST'])
async def login(request: Request):
    """
    登录

    :param request:
    :return:
    """
    await request.receive_body()
    status, result = src.services.userinfo.login(**request.json)
    return Response(status_code=status, data=result).json()
