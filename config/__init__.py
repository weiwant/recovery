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
    'taskinfo',
    'patientinfo',
    'doctorinfo',
    'detailinfo'
]
USE_GPU = True
