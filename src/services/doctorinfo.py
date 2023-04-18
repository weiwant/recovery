from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from src.models.error import DataError
from src.models.mapper import Mapper
from src.models.model import DataModel
from src.services import session_maker, base

fields = Mapper({
    'id': 'id',
    'name': 'name',
    'occupation': 'occupation',
    'workplace': 'workplace',
    'department': 'department',
    'userid': 'userid',
    'profile': 'profile',
    'contact': 'contact'
})


class DoctorService:
    doctor_info = DataModel(__name__, base.classes['doctorinfo'], session_maker, fields.map_dict['id'])
    logger = doctor_info.logger

    @classmethod
    def add_doctor(cls, userid, **kwargs):
        """
        添加医生信息

        :param userid: userid
        :param kwargs: dict
        :return:
        """
        kwargs[fields.map_dict['userid']] = userid
        result = cls.doctor_info.add_record(**kwargs)
        if result is None:
            raise DataError('操作失败')
        return result

    @classmethod
    def get_doc_info(cls, userid):
        """
        获取医生信息

        :param userid: userid
        :return:
        """
        result = cls.doctor_info.get_record(**{fields.map_dict['userid']: userid})
        if result is None:
            raise DataError('操作失败')
        elif not result:
            raise DataError('未找到医生信息')
        return result

    @classmethod
    def show_doctor_info(cls, result, cipher, **kwargs):
        """
        显示医生信息

        :param kwargs: dict
        :param cipher: 加密对象
        :param result: doctorinfo
        :return:
        """
        result.pop(fields.map_dict['id'])
        result[fields.map_dict['userid']] = cipher.encrypt(
            pad(str(result[fields.map_dict['userid']]).encode(), AES.block_size)).hex()
        result.update(kwargs)
        return result
