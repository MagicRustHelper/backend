from datetime import datetime

from pydantic import BaseModel, Field

from app.db.schemas.utils import get_now_datetime


class ReportBase(BaseModel):
    author_nickname: str
    report_steamid: str
    server_number: int
    time: datetime = Field(default_factory=get_now_datetime)


class CreateReport(ReportBase):
    pass


class UpdateReport(ReportBase):
    pass


class Report(ReportBase):
    id: int

    class Config:
        orm_mode = True
