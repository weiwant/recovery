import json


class ModelExt:
    """
    模型扩展基类
    """
    encoder = json.JSONEncoder

    def __repr__(self):
        """
        实例的字符串表示

        :return: str
        """
        fields = self.__dict__
        if '_sa_instance_state' in fields:
            del fields['_sa_instance_state']
        return json.dumps(fields, cls=ModelExt.encoder)
