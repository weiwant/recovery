from Crypto.Hash import MD5
from Crypto.Random import get_random_bytes
from sanic import Request, Blueprint

from src.models.error import ArgError, RuleError, DataError
from src.models.response import Response
from src.services.doctorinfo import doctor_info, fields as doctorinfo_fields
from src.services.patientinfo import patient_info, fields as patientinfo_fields
from src.services.userinfo import user_info, fields as userinfo_fields
from src.utils.logger import get_logger

user_blueprint = Blueprint('user', url_prefix='/user')
key = get_random_bytes(16)
logger = get_logger(__name__)


@user_blueprint.route('/register', methods=['POST'])
async def register(request: Request):
    """
    注册

    :param request:
    :return:
    """
    await request.receive_body()
    args = ['username', 'password', 'type']
    result = None
    try:
        if userinfo_fields.has_values(request.json, args):
            kwargs = userinfo_fields.get_dict(request.json, args)
            if user_info.get_record(
                    **{userinfo_fields.map_dict['username']: kwargs[userinfo_fields.map_dict['username']]}):
                raise RuleError('用户名已存在')
            kwargs[userinfo_fields.map_dict['password']] = MD5.new(
                kwargs[userinfo_fields.map_dict['password']].encode()).hexdigest()
            result = user_info.add_record(**kwargs)
            if result:
                user_type = kwargs[userinfo_fields.map_dict['type']]
                if user_type == 0:
                    pass
                elif user_type == 1:
                    args = ['name', 'occupation', 'workplace', 'department']
                    if doctorinfo_fields.has_values(request.json, args):
                        ext = ['profile', 'contact']
                        kwargs = doctorinfo_fields.get_dict(request.json, args, ext)
                        kwargs[doctorinfo_fields.map_dict['userid']] = result
                        if not doctor_info.add_record(**kwargs):
                            raise DataError('注册失败')
                    else:
                        raise ArgError('缺少参数')
                elif user_type == 2:
                    args = ['name', 'age', 'gender', 'marriage']
                    if patientinfo_fields.has_values(request.json, args):
                        ext = ['contact', 'occupation', 'nationality']
                        kwargs = patientinfo_fields.get_dict(request.json, args, ext)
                        kwargs[patientinfo_fields.map_dict['userid']] = result
                        if not patient_info.add_record(**kwargs):
                            raise DataError('注册失败')
                    else:
                        raise ArgError('缺少参数')
                else:
                    raise DataError('没有这种用户类型')
                return Response(200, message='注册成功').text()
            else:
                raise DataError('注册失败')
        else:
            raise ArgError('缺少参数')
    except (ArgError, DataError, Exception) as e:
        logger.error(f'注册失败: {e}')
        if result:
            user_info.delete_record(**{userinfo_fields.map_dict['id']: result})
        return Response(500, message='注册失败').text()
    except RuleError as e:
        logger.error(f'注册失败: {e}')
        return Response(403, message='用户名已存在').text()


@user_blueprint.route('/login', methods=['POST'])
async def login(request: Request):
    """
    登录

    :param request:
    :return:
    """
    await request.receive_body()
