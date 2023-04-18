from src.models.mapper import Mapper
from src.models.model import DataModel
from src.services import session_maker, base

fields = Mapper({
    'id': 'id',
    'name': 'name',
    'age': 'age',
    'gender': 'gender',
    'marriage': 'marriage',
    'userid': 'userid',
    'contact': 'contact',
    'occupation': 'occupation',
    'nationality': 'nationality'
})
patient_info = DataModel(__name__, base.classes['patientinfo'], session_maker, fields.map_dict['id'])
logger = patient_info.logger
