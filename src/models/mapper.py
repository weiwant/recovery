class Mapper:
    """
    字段映射
    """

    def __init__(self, map_dict):
        """
        初始化

        :param map_dict: 映射字典
        """
        self.map_dict = map_dict
        self.map_dict_reverse = dict(zip(map_dict.values(), map_dict.keys()))

    def has_values(self, dic, key):
        """
        判断字典是否包含指定键

        :param dic: 字典
        :param key: 键
        :return: bool
        """
        if isinstance(key, list):
            return set(dic.keys()).issuperset(set([self.map_dict[k] for k in key]))
        else:
            return self.map_dict[key] in dic.keys()

    def get_dict(self, dic, key, opt):
        """
        获取字典中指定键的值

        :param dic: 字典
        :param key: 键
        :param opt: 选项
        :return: Any
        """
        if isinstance(key, list):
            dic = dict(zip([self.map_dict[k] for k in key], [dic[self.map_dict[k]] for k in key]))
            dic.update([(self.map_dict[k], dic[self.map_dict[k]]) for k in opt if self.map_dict[k] in dic.keys()])
            return
        else:
            return {self.map_dict[key]: dic[self.map_dict[key]]}
