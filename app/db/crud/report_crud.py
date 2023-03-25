from app.db.crud import CRUDBase
from app.db.models import Report
from app.db.schemas import CreateReport, UpdateReport


class CRUDReport(CRUDBase[Report, CreateReport, UpdateReport]):
    pass


report = CRUDReport(Report)
