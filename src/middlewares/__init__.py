from src.middlewares.api import access_log_middleware, response_log_middleware

REQUEST = [
    access_log_middleware
]
RESPONSE = [
    response_log_middleware
]
