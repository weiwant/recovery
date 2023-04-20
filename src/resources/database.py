from casestyle import pascalcase

from config import TABLES
from src.classes.model import DataModel
from src.resources import session_maker, base


class Tables:
    """
    数据表
    """

    def __init__(self):
        """
        初始化
        """
        self.__dict__.update({pascalcase(name): DataModel(name, base.classes[name], session_maker, key_column)
                              for name, key_column in TABLES.items()})
