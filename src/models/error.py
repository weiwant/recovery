class ArgError(Exception):
    """
    参数错误
    """

    def __init__(self, message):
        """
        初始化

        :param message: 错误信息
        """
        self.message = message

    def __str__(self):
        """
        字符串化

        :return:
        """
        return self.message


class RuleError(Exception):
    """
    规则错误
    """

    def __init__(self, message):
        """
        初始化

        :param message: 错误信息
        """
        self.message = message

    def __str__(self):
        """
        字符串化

        :return:
        """
        return self.message


class DataError(Exception):
    """
    数据错误
    """

    def __init__(self, message):
        """
        初始化

        :param message: 错误信息
        """
        self.message = message

    def __str__(self):
        """
        字符串化

        :return:
        """
        return self.message
