"""
@Author: Wenfeng Zhou
"""
from typing import Union

from casestyle import pascalcase
from pydantic import BaseModel
from pydantic.typing import NoneType

from config import TABLES
from src.classes.model import DataModel
from src.resources import session_maker, base


class MetaClass(type):
    """
    元类
    """

    def __new__(mcs, name, bases, attrs):
        """
        创建类

        :param name: 类名
        :param bases: 父类
        :param attrs: 属性
        :return:
        """
        attrs.update({pascalcase(name): DataModel(name, base.classes[name], session_maker, key_column)
                      for name, key_column in TABLES.items()})
        for name in TABLES.keys():
            table = base.classes[name].__dict__['__table__']
            annotations = {}
            for c in getattr(table.columns, '_all_columns'):
                annotations.update({str(c.name): Union[NoneType, c.type.python_type]})
            field_name = pascalcase(name) + 'Field'
            attrs.update({field_name: type(field_name, (BaseModel,), {'__annotations__': annotations})})
        return super().__new__(mcs, name, bases, attrs)


class Tables(metaclass=MetaClass):
    """
    数据表
    """
