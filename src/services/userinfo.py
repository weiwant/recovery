from src.models.mapper import Mapper
from src.models.model import DataModel
from src.services import session_maker, base

user_info = DataModel(__name__, base.classes['userinfo'], session_maker, 'id')
logger = user_info.logger
fields = Mapper({
    'id': 'id',
    'username': 'username',
    'password': 'password',
    'type': 'type'
})
