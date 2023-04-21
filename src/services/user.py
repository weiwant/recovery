from sqlalchemy.orm import Session

from src.classes.model import DataModel
from src.resources import session_maker, base
from src.resources.database import Tables

Userinfo: DataModel = getattr(Tables, 'Userinfo')
user_logger = Userinfo.logger
user_fields = getattr(Tables, 'UserinfoField')
DoctorInfo: DataModel = getattr(Tables, 'DoctorInfo')
doctor_logger = DoctorInfo.logger
doctor_fields = getattr(Tables, 'DoctorInfoField')
PatientInfo: DataModel = getattr(Tables, 'PatientInfo')
patient_logger = PatientInfo.logger
patient_fields = getattr(Tables, 'PatientInfoField')


def add_user(**kwargs):
    """
    添加用户

    :param kwargs: 用户信息
    :return:
    """
    if kwargs.get('nickname', None) is None:
        kwargs['nickname'] = '微信用户'
    if not Userinfo.add_record(**kwargs):
        user_logger.error(f'添加用户失败: {kwargs}')
        raise ValueError(f'添加用户失败: {kwargs}')


def update_user(**kwargs):
    """
    更新用户

    :param kwargs: 用户信息
    :return:
    """
    data = user_fields(**kwargs).dict(exclude_none=True)
    if not Userinfo.update_record(**data):
        user_logger.error(f'更新用户失败: {data}')
        raise ValueError(f'更新用户失败: {data}')
    if kwargs.get('type', None) == 2:
        with session_maker() as session:
            try:
                session: Session
                data = patient_fields(**kwargs).dict(exclude_none=True, exclude={'userid', 'id'})
                session.query(base.classes['patient_info']).filter_by(userid=kwargs['openid']).update(data)
                session.commit()
            except Exception as e:
                patient_logger.error(f'更新患者信息失败: {e}')
                raise ValueError(f'更新患者信息失败: {e}')
    elif kwargs.get('type', None) == 3:
        with session_maker() as session:
            try:
                session: Session
                data = doctor_fields(**kwargs).dict(exclude_none=True, exclude={'userid', 'id'})
                session.query(base.classes['doctor_info']).filter_by(userid=kwargs['openid']).update(data)
                session.commit()
            except Exception as e:
                doctor_logger.error(f'更新医生信息失败: {e}')
                raise ValueError(f'更新医生信息失败: {e}')


def get_user(**kwargs):
    """
    获取用户

    :param kwargs: 用户信息
    :return:
    """
    result = Userinfo.get_record(**kwargs)
    if result is None:
        user_logger.error(f'获取用户失败: {kwargs}')
        raise ValueError(f'获取用户失败: {kwargs}')
    if result:
        result = result[0].to_json()
        openid = result['openid']
        result = user_fields(**result).dict(exclude_none=True, exclude={'openid', 'session_key'})
        user_type = result['type']
        addition = {}
        if user_type == 0:
            pass
        elif user_type == 1:
            pass
        elif user_type == 2:
            temp = PatientInfo.get_record(userid=openid)
            if temp is None:
                patient_logger.error(f'获取患者信息失败: {openid}')
                raise ValueError(f'获取患者信息失败: {openid}')
            if temp:
                addition = patient_fields(**temp[0].to_json()).dict(exclude_none=True, exclude={'userid', 'id'})
        elif user_type == 3:
            temp = DoctorInfo.get_record(userid=openid)
            if temp is None:
                doctor_logger.error(f'获取医生信息失败: {openid}')
                raise ValueError(f'获取医生信息失败: {openid}')
            if temp:
                addition = doctor_fields(**temp[0].to_json()).dict(exclude_none=True, exclude={'userid', 'id'})
        else:
            user_logger.error(f'用户类型错误: {user_type}')
            raise ValueError(f'用户类型错误: {user_type}')
        result.update(addition)
    return result


def delete_user(**kwargs):
    """
    删除用户

    :param kwargs: 用户信息
    :return:
    """
    if not Userinfo.delete_record(**kwargs):
        user_logger.error(f'删除用户失败: {kwargs}')
        raise ValueError(f'删除用户失败: {kwargs}')


def exist_user(**kwargs):
    """
    用户是否存在

    :param kwargs: 用户信息
    :return:
    """
    return len(Userinfo.get_record(**kwargs)) > 0


def add_patient(**kwargs):
    """
    添加患者

    :param kwargs: 患者信息
    :return:
    """
    if PatientInfo.add_record(**patient_fields(**kwargs).dict(exclude_none=True, exclude={'id'})) is None:
        patient_logger.error(f'添加患者失败: {kwargs}')
        raise ValueError(f'添加患者失败: {kwargs}')


def add_doctor(**kwargs):
    """
    添加医生

    :param kwargs: 医生信息
    :return:
    """
    if DoctorInfo.add_record(**doctor_fields(**kwargs).dict(exclude_none=True, exclude={'id'})) is None:
        doctor_logger.error(f'添加医生失败: {kwargs}')
        raise ValueError(f'添加医生失败: {kwargs}')
