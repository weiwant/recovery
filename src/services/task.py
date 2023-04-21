from sqlalchemy.orm.session import Session

from src.classes.model import DataModel
from src.resources import session_maker, base
from src.resources.database import Tables

TaskInfo: DataModel = getattr(Tables, 'TaskInfo')
task_logger = TaskInfo.logger
task_fields = getattr(Tables, 'TaskInfoField')
DoctorInfo: DataModel = getattr(Tables, 'DoctorInfo')
doctor_logger = DoctorInfo.logger
doctor_fields = getattr(Tables, 'DoctorInfoField')
PatientInfo: DataModel = getattr(Tables, 'PatientInfo')
patient_logger = PatientInfo.logger
patient_fields = getattr(Tables, 'PatientInfoField')


def update_task(**kwargs):
    """
    更新任务

    :param kwargs: 任务参数
    :return:
    """
    if not TaskInfo.update_record(**kwargs):
        task_logger.error(f'更新任务失败: {kwargs}')
        raise ValueError(f'更新任务失败: {kwargs}')


def add_task(**kwargs):
    """
    添加任务

    :param kwargs: 任务参数
    :return:
    """
    if not TaskInfo.add_record(**kwargs):
        task_logger.error(f'添加任务失败: {kwargs}')
        raise ValueError(f'添加任务失败: {kwargs}')


def delete_task(**kwargs):
    """
    删除任务

    :param kwargs: 任务参数
    :return:
    """
    if not TaskInfo.delete_record(**kwargs):
        task_logger.error(f'删除任务失败: {kwargs}')
        raise ValueError(f'删除任务失败: {kwargs}')


def get_task(**kwargs):
    """
    获取任务

    :param kwargs: 任务参数
    :return:
    """
    with session_maker() as session:
        try:
            session: Session
            return session.query(base.classes['task_info']).filter_by(
                **task_fields(**kwargs).dict(exclude_none=True)).all()
        except Exception as e:
            task_logger.error(f'获取任务失败: {e}')
            raise ValueError(f'获取任务失败: {e}')
