"""
@Author: Wenfeng Zhou, Ye Huang
"""
import json

import hashids
import requests
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
User_bind: DataModel = getattr(Tables, 'UserBind')
user_bind_logger = User_bind.logger
TaskInfo: DataModel = getattr(Tables, 'TaskInfo')
task_logger = TaskInfo.logger
task_fields = getattr(Tables, 'TaskInfoField')


def add_user(**kwargs):
    """
    添加用户

    :author: Ye Huang
    :param kwargs: 用户信息
    :return:
    """

    url_code2Session = "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}" \
                       "&grant_type=authorization_code".format(kwargs['appid'], kwargs['secret'], kwargs['code'])
    data = requests.get(url_code2Session)
    if data.status_code == 200:
        data_content = json.loads(data.content)
        if 'session_key' in data_content:
            session_key = data_content['session_key']
            kwargs.update({'session_key': session_key})
        if 'openid' in data_content:
            openid = data_content['openid']
            openid = hashids.Hashids(min_length=16, salt='dcghjjhggggio').encode(openid)
            kwargs.update({'openid': openid})

    if not Userinfo.add_record(**user_fields(**kwargs).dict(exclude_none=True)):
        user_logger.error(f'添加用户失败: {kwargs}')
        raise ValueError(f'添加用户失败: {kwargs}')


def update_user(**kwargs):
    """
    更新用户

    :author: Wenfeng Zhou
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

    :author: Wenfeng Zhou
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

    :author: Wenfeng Zhou
    :param kwargs: 用户信息
    :return:
    """
    if not Userinfo.delete_record(**kwargs):
        user_logger.error(f'删除用户失败: {kwargs}')
        raise ValueError(f'删除用户失败: {kwargs}')


def exist_user(**kwargs):
    """
    用户是否存在

    :author: Wenfeng Zhou
    :param kwargs: 用户信息
    :return:
    """
    return len(Userinfo.get_record(**kwargs)) > 0


def add_patient(**kwargs):
    """
    添加患者数据

    :author: Wenfeng Zhou
    :param kwargs: 患者信息
    :return:
    """
    if PatientInfo.add_record(**patient_fields(**kwargs).dict(exclude_none=True, exclude={'id'})) is None:
        patient_logger.error(f'添加患者失败: {kwargs}')
        raise ValueError(f'添加患者失败: {kwargs}')


def add_doctor(**kwargs):
    """
    添加医生数据

    :author: Wenfeng Zhou
    :param kwargs: 医生信息
    :return:
    """
    if DoctorInfo.add_record(**doctor_fields(**kwargs).dict(exclude_none=True, exclude={'id'})) is None:
        doctor_logger.error(f'添加医生失败: {kwargs}')
        raise ValueError(f'添加医生失败: {kwargs}')


def bind_user(**kwargs):
    """
    添加医患绑定

    :author: Ye Huang
    :param kwargs:
    :return:
    """
    if not len(User_bind.get_record(**kwargs)) == 0:
        user_bind_logger.error(f'已绑定:{kwargs}')
        raise ValueError(f'已绑定:{kwargs}')
    else:
        if User_bind.add_record(**kwargs) is None:
            user_bind_logger.error(f'绑定失败:{kwargs}')
            raise ValueError(f'绑定失败:{kwargs}')


def get_doctor(**kwargs):
    """
    获取我的医生列表

    :author: Ye Huang
    :param kwargs: patient
    :return:
    """
    if len(User_bind.get_record(**kwargs)) == 0:
        user_bind_logger.error(f'无内容:{kwargs}')
        raise ValueError(f'无内容:{kwargs}')
    else:
        result = []
        res = User_bind.get_record(**kwargs)
        for item in res:
            id_dict = {'openid': item.doctor}
            info_dict = {'id': item.doctor}
            user = Userinfo.get_record(**id_dict)
            info_dict.update({'imgUrl': user[0].img})
            doc = DoctorInfo.get_record(**{'userid': item.doctor})
            info_dict.update({'name': doc[0].name})
            info_dict.update({'hospital': doc[0].hospital})
            result.append(info_dict)
        return result


def get_patient(**kwargs):
    """
    获取医生的患者列表

    :author: Ye Huang
    :param kwargs: doctor
    :return:
    """
    if len(User_bind.get_record(**kwargs)) == 0:
        user_bind_logger.error(f'无内容:{kwargs}')
        raise ValueError(f'无内容:{kwargs}')
    else:
        result = []
        res = User_bind.get_record(**kwargs)
        for item in res:
            user_dict = {}
            user = Userinfo.get_record(**{'openid': item.patient})
            user_dict.update({'patientId': item.patient})
            user_dict.update({'patientName': user[0].nickname})
            user_dict.update({'patientImg': user[0].img})
            taskList = []
            people = {'doctor': kwargs['doctor'], 'patient': item.patient}
            task = TaskInfo.get_record(**people)
            for t in task:
                task_dict = {'taskName': t.type}
                task_dict.update({'taskid': t.id})
                taskList.append(task_dict)
            user_dict.update({'tasklist': taskList})
            result.append(user_dict)
        return result
