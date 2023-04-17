from src.models.mapper import Mapper
from src.models.model import DataModel
from src.services import session_maker, base

doctor_info = DataModel(__name__, base.classes['doctorinfo'], session_maker, 'id')
logger = doctor_info.logger
fields = Mapper({
    'id': 'id',
    'name': 'name',
    'occupation': 'occupation',
    'workplace': 'workplace',
    'department': 'department',
    'userid': 'userid',
    'profile': 'profile',
    'contact': 'contact'
})
