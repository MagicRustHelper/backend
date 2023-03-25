from app.db.crud import CRUDBase
from app.db.models import Check
from app.db.schemas import CreateCheck, UpdateCheck


class CRUDCheck(CRUDBase[Check, CreateCheck, UpdateCheck]):
    pass


check = CRUDCheck(Check)
