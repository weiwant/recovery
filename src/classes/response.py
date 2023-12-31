"""
@Author: Wenfeng Zhou
"""
import json as _json
from datetime import date

from sanic import json, text, empty

from src.utils.encoder import JSONEncoder
from src.utils.model import ModelExt


class Response:
    """
    响应类
    """
    extensions = [
        (ModelExt, lambda o: _json.loads(o.__repr__())),
        (date, lambda o: str(o))
    ]

    def __init__(self, status_code: int = 200, message: str = None, data=None):
        """
        构造响应结果

        :param status_code: HTTP响应码
        :param message: 消息内容
        :param data: 数据
        """
        self.status = status_code
        self.message = message
        self.data = data

    def json(self):
        """
        响应的json表示

        :return: json
        """
        setattr(JSONEncoder, 'ext', Response.extensions)
        return json(_json.loads(_json.dumps(self.data, cls=JSONEncoder)), status=self.status)

    def text(self):
        """
        响应的字符串表示

        :return: str
        """
        return text(self.message, status=self.status)

    def empty(self):
        """
        响应的空表示

        :return: empty
        """
        return empty(status=self.status)
