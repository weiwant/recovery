from src.models.mapper import Mapper
from src.models.model import DataModel
from src.services import session_maker, base

fields = Mapper({
    'id': 'id',
    'username': 'username',
    'password': 'password',
    'type': 'type',
    'iv': 'iv',
    'login_host': 'loginhost'
})
user_info = DataModel(__name__, base.classes['userinfo'], session_maker, fields.map_dict['id'])
logger = user_info.logger
