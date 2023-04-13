def get_connect_string(dbtype, user='', host='', password='', driver='', dbname='', port='', path='', **kwargs):
    """
    构造数据库连接字符串

    :param dbtype: 数据库类型
    :param user: 用户名
    :param host: 连接主机
    :param password: 密码
    :param driver: 数据库驱动
    :param dbname: 数据库名字
    :param port: 端口
    :param path: 数据库文件路径
    :param kwargs: 额外设定
    :return: str
    """
    if path == '' and (user == '' or host == '' or password == ''):
        raise Exception('Could not get connect string')
    options = ('?' + ''.join([k + '=' + kwargs[k] + '&' for k in kwargs]).removesuffix('&')) if kwargs else ''
    db_url = user + ':' + password + '@' + host + ((':' + port) if not port == '' else '') + '/' + (
        dbname if not dbname == '' else '')
    db_path = (':' + password + '@' + path) if not password == '' else path
    return dbtype + (('+' + driver) if not driver == '' else '') + '://' + (
        db_path if not path == '' else db_url) + options
