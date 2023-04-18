from sanic import Request, Blueprint

from config import key
from src.models.error import ArgError, RuleError, DataError
from src.models.response import Response
from src.services.doctorinfo import DoctorService
from src.services.doctorinfo import fields as doctorinfo_fields
from src.services.patientinfo import PatientService
from src.services.patientinfo import fields as patientinfo_fields
from src.services.userinfo import UserService
from src.services.userinfo import fields as userinfo_fields
from src.utils.logger import get_logger

user_blueprint = Blueprint('user', url_prefix='/user')
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
            result = UserService.add_user(**kwargs)
            user_type = kwargs[userinfo_fields.map_dict['type']]
            if user_type == 0:
                pass
            elif user_type == 1:
                args = ['name', 'occupation', 'workplace', 'department']
                ext = ['profile', 'contact']
                if doctorinfo_fields.has_values(request.json, args):
                    kwargs = doctorinfo_fields.get_dict(request.json, args, ext)
                    DoctorService.add_doctor(result, **kwargs)
                else:
                    raise ArgError('缺少参数')
            elif user_type == 2:
                args = ['name', 'age', 'gender', 'marriage']
                ext = ['contact', 'occupation', 'nationality']
                if patientinfo_fields.has_values(request.json, args):
                    kwargs = patientinfo_fields.get_dict(request.json, args, ext)
                    PatientService.add_patient(result, **kwargs)
                else:
                    raise ArgError('缺少参数')
            else:
                raise ArgError('没有这种用户类型')
            return Response(200, message='注册成功').text()
        else:
            raise ArgError('缺少参数')
    except RuleError as e:
        logger.error(f'注册失败: {e}')
        return Response(403, message='用户名已存在').text()
    except (ArgError, DataError, Exception) as e:
        logger.error(f'注册失败: {e}')
        if result:
            UserService.delete_user(result)
        return Response(500, message='注册失败').text()


@user_blueprint.route('/login', methods=['POST'])
async def login(request: Request):
    """
    登录

    :param request:
    :return:
    """
    await request.receive_body()
    args = ['username', 'password']
    try:
        if userinfo_fields.has_values(request.json, args):
            kwargs = userinfo_fields.get_dict(request.json, args)
            result = UserService.get_user_info(**kwargs)
            user_type = getattr(result[0], userinfo_fields.map_dict['type'])
            user_id = getattr(result[0], userinfo_fields.map_dict['id'])
            user_name = getattr(result[0], userinfo_fields.map_dict['username'])
            cipher = UserService.update_login(user_id, key, request.host)
            usr_info = None
            if user_type == 0:
                pass
            elif user_type == 1:
                usr_info = DoctorService.get_doc_info(user_id)
                usr_info = DoctorService.show_doctor_info(usr_info[0].to_json(), cipher, **{
                    userinfo_fields.map_dict['username']: user_name,
                    userinfo_fields.map_dict['type']: user_type
                })
            elif user_type == 2:
                usr_info = PatientService.get_patient(user_id)
                usr_info = PatientService.show_patient_info(usr_info[0].to_json(), cipher, **{
                    userinfo_fields.map_dict['username']: user_name,
                    userinfo_fields.map_dict['type']: user_type
                })
            else:
                raise ArgError('没有这种用户类型')
            return Response(200, data=usr_info).json()
        else:
            raise ArgError('缺少参数')
    except RuleError as e:
        logger.error(f'登录失败: {e}')
        return Response(403, message='用户名或密码错误').text()
    except (ArgError, DataError, Exception) as e:
        logger.error(f'登录失败: {e}')
        return Response(500, message='登录失败').text()
