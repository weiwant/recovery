"""
@Author: Wenfeng Zhou
"""
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
    'detail_info': 'id',
    'user_bind': 'id',
    'articles': 'id',
    'comments': 'id',
    'posts': 'id',
    'likes': 'id',
    'collect': 'id'
}
TASK = {
    '坐姿抬腿训练': 'sit_lift_leg',
    '躺下抬腿训练': 'lie_lift_leg',
    '躺下开合腿训练': 'lie_open_leg'
}
USE_GPU = True
OPENPOSE_ROOT = 'openpose-1.7.0'
key = get_random_bytes(16)
