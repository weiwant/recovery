from Crypto.Random import get_random_bytes

DATABASE_CONFIG = {
    'dbtype': 'mysql',
    'user': 'Manager',
    'host': 'localhost',
    'password': '123456',
    'driver': 'pymysql',
    'dbname': 'recovery',
    'port': '3306'
}
TABLES = {
    'userinfo': 'openid',
    'task_info': 'id',
    'patient_info': 'id',
    'doctor_info': 'id',
    'detail_info': 'id'
}
USE_GPU = True
key = get_random_bytes(16)
