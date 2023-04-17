from src.models.mapper import Mapper
from src.models.model import DataModel
from src.services import session_maker, base

patient_info = DataModel(__name__, base.classes['patientinfo'], session_maker, 'id')
logger = patient_info.logger
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
