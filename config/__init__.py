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
TABLES = [
    'userinfo',
    'task_info',
    'patient_info',
    'doctor_info',
    'detail_info'
]
USE_GPU = True
key = get_random_bytes(16)
