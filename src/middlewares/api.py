"""
@Author: Wenfeng Zhou
"""
from sanic import Request

from src.utils.logger import get_logger

logger = get_logger(__name__)


async def access_log_middleware(request: Request):
    """
    记录访问日志
    """
    logger.info(f'访问: {request.path}')


async def response_log_middleware(request: Request, response):
    """
    记录响应日志
    """
    logger.info(f'响应: {request.path} {response.status}')
