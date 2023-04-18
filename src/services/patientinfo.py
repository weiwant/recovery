from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from src.models.error import DataError
from src.models.mapper import Mapper
from src.models.model import DataModel
from src.services import session_maker, base

fields = Mapper({
    'id': 'id',
    'name': 'name',
    'age': 'age',
    'gender': 'gender',
    'marriage': 'marriage',
    'userid': 'userid',
    'contact': 'contact',
    'occupation': 'occupation',
    'nationality': 'nationality'
})


class PatientService:
    patient_info = DataModel(__name__, base.classes['patientinfo'], session_maker, fields.map_dict['id'])
    logger = patient_info.logger

    @classmethod
    def add_patient(cls, userid, **kwargs):
        """
        添加病人信息

        :param userid: userid
        :param kwargs: dict
        :return:
        """
        kwargs[fields.map_dict['userid']] = userid
        result = cls.patient_info.add_record(**kwargs)
        if result is None:
            raise DataError('操作失败')
        return result

    @classmethod
    def get_patient(cls, userid):
        """
        获取病人信息

        :param userid: userid
        :return:
        """
        result = cls.patient_info.get_record(**{fields.map_dict['userid']: userid})
        if result is None:
            raise DataError('操作失败')
        elif not result:
            raise DataError('未找到病人信息')
        return result

    @classmethod
    def show_patient_info(cls, result, cipher, **kwargs):
        """
        显示病人信息

        :param kwargs: dict
        :param cipher: 加密对象
        :param result: result
        :return:
        """
        result[fields.map_dict['userid']] = cipher.encrypt(
            pad(str(result[fields.map_dict['userid']]).encode(), AES.block_size)).hex()
        result.pop(fields.map_dict['id'])
        result.update(kwargs)
        return result
