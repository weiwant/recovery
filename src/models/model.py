from sqlalchemy import update
from sqlalchemy.orm import Session

from src.utils.logger import get_logger


class DataModel:
    """
    数据模型
    """

    def __init__(self, name, class_, session_maker, key_column):
        """
        初始化

        :param name: data model name
        :param class_: data model class
        :param session_maker: data model session maker
        :param key_column: data model key column
        """
        self.logger = get_logger(name)
        self.class_ = class_
        self.session_maker = session_maker
        self.key = key_column

    def add_record(self, **kwargs):
        """
        添加记录

        :param kwargs: record
        :return:
        """
        with self.session_maker() as session:
            try:
                session: Session
                record = self.class_(**kwargs)
                session.add(record)
                session.commit()
                return getattr(record, self.key)
            except Exception as e:
                self.logger.error(f'添加 {self.class_.__name__} 记录失败: {e}')
                return None

    def delete_record(self, **kwargs):
        """
        删除记录

        :param kwargs: record
        :return:
        """
        with self.session_maker() as session:
            try:
                session: Session
                key = kwargs.pop(self.key)
                session.query(self.class_).filter_by(**{self.key: key}).delete()
                session.commit()
            except Exception as e:
                self.logger.error(f'删除 {self.class_.__name__} 记录失败: {e}')

    def update_record(self, **kwargs):
        """
        更新记录

        :param kwargs: record
        :return:
        """
        with self.session_maker() as session:
            try:
                session: Session
                if self.key not in kwargs:
                    raise ValueError(f'更新 {self.class_.__name__} 记录失败: 缺少关键字参数 {self.key}')
                session.execute(update(self.class_), [kwargs])
                session.commit()
            except Exception as e:
                self.logger.error(f'更新 {self.class_.__name__} 记录失败: {e}')

    def get_record(self, **kwargs):
        """
        获取记录

        :param kwargs: record
        :return:
        """
        with self.session_maker() as session:
            try:
                session: Session
                return session.query(self.class_).filter_by(**kwargs).all()
            except Exception as e:
                self.logger.error(f'获取 {self.class_.__name__} 记录失败: {e}')
                return None
