from logging import getLogger

import sanic

logger = getLogger(__name__)

api_blueprint = sanic.blueprints.Blueprint('api', url_prefix='/recovery/api')
method_get = {}
method_post = {}
for (k, v) in method_get.items():
    api_blueprint.add_route(v, k)
for (k, v) in method_post.items():
    api_blueprint.add_route(v, k, methods=['POST'])
logger.info('蓝图注册成功')
