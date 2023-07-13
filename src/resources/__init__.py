"""
@Author: Wenfeng Zhou
"""
import os
import sys
from datetime import date
from sys import platform

from src import config
from src.utils.encoder import JSONEncoder
from src.utils.logger import get_logger
from src.utils.model import ModelExt

logger = get_logger(__name__)
if hasattr(config, 'USE_GPU') and hasattr(config, 'OPENPOSE_ROOT'):
    from src.config import USE_GPU, OPENPOSE_ROOT

    dir_name = OPENPOSE_ROOT
    build_dir = 'build_GPU' if USE_GPU else 'build_CPU'
    if platform == 'win32':
        bin_dir = os.path.join(dir_name, build_dir, 'bin')
        dll_dir = os.path.join(dir_name, build_dir, 'x64', 'Release')
        os.environ['PATH'] = os.environ['PATH'] + ';' + bin_dir + ';' + dll_dir
        sys.path.append(os.path.join(dir_name, build_dir, 'python', 'openpose', 'Release'))
    else:
        sys.path.append(os.path.join('./', dir_name, build_dir, 'python'))
if hasattr(config, 'DATABASE_CONFIG') and hasattr(config, 'TABLES'):
    from sqlalchemy import create_engine, MetaData
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import sessionmaker

    from src.config import DATABASE_CONFIG, TABLES
    from src.utils.database import get_connect_string

    connect_string = get_connect_string(**DATABASE_CONFIG)
    engine = create_engine(connect_string)
    meta = MetaData()
    meta.reflect(engine, only=TABLES.keys())
    setattr(JSONEncoder, 'ext', [
        (date, lambda o: str(o))
    ])
    setattr(ModelExt, 'encoder', JSONEncoder)
    base = automap_base(metadata=meta, cls=ModelExt)
    base.prepare()
    session_maker = sessionmaker(engine, expire_on_commit=False)
    logger.info('获取数据库连接成功')
