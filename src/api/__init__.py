import sanic

from src.utils.logger import get_logger

logger = get_logger(__name__)

api_blueprint = sanic.blueprints.Blueprint('api', url_prefix='/recovery/api')
api_group = sanic.blueprints.BlueprintGroup(url_prefix='/recovery/api')
method_get = {}
method_post = {}
blueprints = []
for (k, v) in method_get.items():
    api_blueprint.add_route(v, k)
    logger.info(f'API GET {k} 注册成功')
for (k, v) in method_post.items():
    api_blueprint.add_route(v, k, methods=['POST'])
    logger.info(f'API POST {k} 注册成功')
for blueprint in blueprints:
    api_group.append(blueprint)
    logger.info(f'API Group {blueprint.name} 注册成功')
