from logging import getLogger, StreamHandler

import sanic
from sanic_cors import CORS

from src.api import api_blueprint
from src.middlewares import REQUEST, RESPONSE

logger = getLogger(__name__)
logger.setLevel('INFO')
logger.addHandler(StreamHandler())
app = sanic.Sanic(__name__)
app.blueprint(api_blueprint)
for middleware in REQUEST:
    app.on_request(middleware)
    logger.info(f'请求中间件{middleware.__name__}注册成功')
for middleware in RESPONSE:
    app.on_response(middleware)
    logger.info(f'响应中间件{middleware.__name__}注册成功')
CORS(app)
logger.info('CORS注册成功')
