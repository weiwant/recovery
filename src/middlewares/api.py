"""
@Author: Wenfeng Zhou
"""
import time

from sanic import Request

from src.utils.logger import get_logger

logger = get_logger(__name__)
record_time = 0


async def access_log_middleware(request: Request):
    """
    记录访问日志
    """
    logger.info(f'访问: {request.method} {request.path}')
    global record_time
    record_time = time.time()


async def response_log_middleware(request: Request, response):
    """
    记录响应日志
    """
    logger.info(f'响应: {request.method} {request.path} {response.status}')
    global record_time
    logger.info(f'响应时间: {time.time() - record_time}')
