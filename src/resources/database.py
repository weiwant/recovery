from casestyle import pascalcase

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

        :param mcs: 元类
        :param name: 类名
        :param bases: 父类
        :param attrs: 属性
        :return:
        """
        attrs.update({pascalcase(name): DataModel(name, base.classes[name], session_maker, key_column)
                      for name, key_column in TABLES.items()})
        return super().__new__(mcs, name, bases, attrs)


class Tables(metaclass=MetaClass):
    """
    数据表
    """
