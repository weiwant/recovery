import json
import os
import shutil
from datetime import date, datetime

from Crypto.Hash import SHA256

from src.classes.model import DataModel
from src.resources.database import Tables

TaskInfo: DataModel = getattr(Tables, 'TaskInfo')
task_logger = TaskInfo.logger
task_fields = getattr(Tables, 'TaskInfoField')


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
    kwargs['status'] = 0
    kwargs['create_date'] = date.today()
    kwargs['training_root'] = SHA256.new((str(datetime.now()) + json.dumps(kwargs)).encode()).hexdigest()
    kwargs['evaluate_root'] = SHA256.new((str(datetime.now()) + json.dumps(kwargs)).encode()).hexdigest()
    if TaskInfo.add_record(**kwargs) is None:
        task_logger.error(f'添加任务失败: {kwargs}')
        raise ValueError(f'添加任务失败: {kwargs}')
    if not os.path.exists(f'./training/{kwargs["training_root"]}'):
        os.makedirs(f'./training/{kwargs["training_root"]}')
    if not os.path.exists(f'./evaluation/{kwargs["evaluate_root"]}'):
        os.makedirs(f'./evaluation/{kwargs["evaluate_root"]}')


def delete_task(**kwargs):
    """
    删除任务

    :param kwargs: 任务参数
    :return:
    """
    temp = TaskInfo.get_record(id=kwargs['id'])[0].to_json()
    training_root = temp['training_root']
    evaluate_root = temp['evaluate_root']
    if not TaskInfo.delete_record(**kwargs):
        task_logger.error(f'删除任务失败: {kwargs}')
        raise ValueError(f'删除任务失败: {kwargs}')
    if os.path.exists(f'./training/{training_root}'):
        shutil.rmtree(f'./training/{training_root}')
    if os.path.exists(f'./evaluation/{evaluate_root}'):
        shutil.rmtree(f'./evaluation/{evaluate_root}')


def get_task(**kwargs):
    """
    获取任务

    :param kwargs: 任务参数
    :return:
    """
    result = TaskInfo.get_record(**task_fields(**kwargs).dict(exclude_none=True))
    if result is None:
        task_logger.error(f'获取任务失败: {kwargs}')
        raise ValueError(f'获取任务失败: {kwargs}')
    return result
