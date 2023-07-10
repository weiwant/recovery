"""
@Author: Wenfeng Zhou
"""
import sanic
from sanic_cors import CORS

from src.api import api_blueprint, api_group
from src.middlewares import REQUEST, RESPONSE
from src.utils.logger import get_logger

logger = get_logger(__name__)
app = sanic.Sanic(__name__)
app.blueprint(sanic.Blueprint.group(api_blueprint, api_group))
for middleware in REQUEST:
    app.on_request(middleware)
    logger.info(f'请求中间件{middleware.__name__}注册成功')
for middleware in RESPONSE:
    app.on_response(middleware)
    logger.info(f'响应中间件{middleware.__name__}注册成功')
CORS(app)
logger.info('CORS注册成功')
