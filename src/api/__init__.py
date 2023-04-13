from logging import getLogger, StreamHandler

import sanic

logger = getLogger(__name__)
logger.setLevel('INFO')
logger.addHandler(StreamHandler())

api_blueprint = sanic.blueprints.Blueprint('api', url_prefix='/recovery/api')
method_get = {}
method_post = {}
for (k, v) in method_get.items():
    api_blueprint.add_route(v, k)
    logger.info(f'API GET {k} 注册成功')
for (k, v) in method_post.items():
    api_blueprint.add_route(v, k, methods=['POST'])
    logger.info(f'API POST {k} 注册成功')
