"""
@Author: Wenfeng Zhou
"""
import os.path
from uuid import uuid4

from src.classes.model import DataModel
from src.resources.database import Tables

DetailInfo: DataModel = getattr(Tables, 'DetailInfo')
detail_logger = DetailInfo.logger
detail_fields = getattr(Tables, 'DetailInfoField')
TaskInfo: DataModel = getattr(Tables, 'TaskInfo')
task_logger = TaskInfo.logger
task_fields = getattr(Tables, 'TaskInfoField')


def add_detail(**kwargs):
    """
    添加任务详情

    :param kwargs: 任务详情参数
    :return:
    """
    result = DetailInfo.add_record(**detail_fields(**kwargs).dict(exclude_none=True))
    if result is None:
        detail_logger.error(f'添加任务详情失败: {kwargs}')
        raise ValueError(f'添加任务详情失败: {kwargs}')
    if kwargs['deadline'] == kwargs['finish_date']:
        if not TaskInfo.update_record(**{'id': kwargs['task'], 'status': 2}):
            task_logger.error(f'更新任务失败: {kwargs}')
            raise ValueError(f'更新任务失败: {kwargs}')
    elif kwargs['status'] == 0:
        if not TaskInfo.update_record(**{'id': kwargs['task'], 'status': 1}):
            task_logger.error(f'更新任务失败: {kwargs}')
            raise ValueError(f'更新任务失败: {kwargs}')


def get_detail(**kwargs):
    """
    获取任务详情

    :param kwargs: 任务详情参数
    :return:
    """
    result = DetailInfo.get_record(**detail_fields(**kwargs).dict(exclude_none=True))
    if result is None:
        detail_logger.error(f'获取任务详情失败: {kwargs}')
        raise ValueError(f'获取任务详情失败: {kwargs}')
    return result


def upload_video(**kwargs):
    """
    上传文件

    :param kwargs: 任务详情参数
    :return:
    """
    file = kwargs['video']
    training_root = kwargs['training_root']
    file_name = uuid4().hex + '.' + kwargs['video_type']
    file_path = f'./training/{training_root}/{file_name}'
    if not os.path.exists(f'./training/{training_root}'):
        os.makedirs(f'./training/{training_root}')
    with open(file_path, 'wb') as f:
        f.write(file.body)
    return file_name


def update_detail(**kwargs):
    """
    更新任务详情

    :param kwargs: 任务详情参数
    :return:
    """
    if not DetailInfo.update_record(**detail_fields(**kwargs).dict(exclude_none=True)):
        detail_logger.error(f'更新任务详情失败: {kwargs}')
        raise ValueError(f'更新任务详情失败: {kwargs}')
    try:
        if kwargs['deadline'] == kwargs['finish_date']:
            TaskInfo.update_record(**{'id': kwargs['task'], 'status': 2})
        elif kwargs['status'] == 0:
            TaskInfo.update_record(**{'id': kwargs['task'], 'status': 1})
    except Exception:
        detail_logger.error(f'更新任务失败: {kwargs}')
        raise ValueError(f'更新任务失败: {kwargs}')
