"""
@Author: Wenfeng Zhou
"""
import json

from typing import List


class JSONEncoder(json.JSONEncoder):
    """
    自定义JSON序列化编码器
    """
    ext: List[tuple] = None

    def default(self, o):
        """
        处理序列化类型

        :param o: 待序列化数据
        :return: Any
        """
        for item in JSONEncoder.ext:
            if isinstance(o, item[0]):
                return item[1](o)
        return super(JSONEncoder, self).default(o)
