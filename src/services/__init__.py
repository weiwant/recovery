from logging import getLogger, StreamHandler

import config
from src.models.model import ModelExt

logger = getLogger(__name__)
logger.setLevel('INFO')
logger.addHandler(StreamHandler())
if hasattr(config, 'DATABASE_CONFIG') and hasattr(config, 'TABLES'):
    from sqlalchemy import create_engine, MetaData
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import sessionmaker

    from config import DATABASE_CONFIG, TABLES
    from src.utils.database import get_connect_string

    connect_string = get_connect_string(**DATABASE_CONFIG)
    engine = create_engine(connect_string)
    meta = MetaData()
    meta.reflect(engine, only=TABLES)
    base = automap_base(metadata=meta, cls=ModelExt)
    base.prepare()
    session_maker = sessionmaker(engine, expire_on_commit=False)
    logger.info('获取数据库连接成功')
