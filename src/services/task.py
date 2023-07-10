import os
import shutil

from src.classes.model import DataModel
from src.resources.database import Tables

TaskInfo: DataModel = getattr(Tables, 'TaskInfo')
task_logger = TaskInfo.logger
task_fields = getattr(Tables, 'TaskInfoField')
DetailInfo: DataModel = getattr(Tables, 'DetailInfo')
detail_logger = DetailInfo.logger
detail_fields = getattr(Tables, 'DetailInfoField')
Userinfo: DataModel = getattr(Tables, 'Userinfo')
user_logger = Userinfo.logger
user_fields = getattr(Tables, 'UserinfoField')


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
    training_root = kwargs['training_root']
    evaluate_root = kwargs['evaluate_root']
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
    else:
        reslist = []
        for item in result:
            temp = item.to_json()
            info_dict = {'openid': temp['doctor']}
            res1 = Userinfo.get_record(**info_dict)
            temp1 = res1[0].to_json()
            temp.update(url=temp1['img'])
            dict1 = {'task': temp['id']}
            res2 = DetailInfo.get_record(**dict1)
            count = len(res2)
            if count == 0:
                temp.update(done=0)
            else:
                temp.update(done=count)
            reslist.append(temp)
    return reslist


def get_task_info(**kwargs):
    res = TaskInfo.get_record(**kwargs)
    if len(res) == 0:
        task_logger.error(f'获取任务失败: {kwargs}')
        raise ValueError(f'获取任务失败: {kwargs}')
    else:
        info_dict = {}
        info_dict.update({'ddl': res[0].deadline})
        info_dict.update({'name': res[0].type})
        info_dict.update({'diff': res[0].difficulty})
        info_dict.update({'all': res[0].circle_time})
        info_dict.update({'detail': res[0].description})
        done = len(DetailInfo.get_record(**{'task': kwargs['id']}))
        info_dict.update({'done': done})
        return info_dict
