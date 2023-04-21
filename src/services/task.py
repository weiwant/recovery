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
    if TaskInfo.add_record(**kwargs) is None:
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
    result = TaskInfo.get_record(**task_fields(**kwargs).dict(exclude_none=True))
    if result is None:
        task_logger.error(f'获取任务失败: {kwargs}')
        raise ValueError(f'获取任务失败: {kwargs}')
    return result
