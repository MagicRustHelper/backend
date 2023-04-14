from pydantic import BaseModel


class ReportBase(BaseModel):
    author_nickname: str
    report_steamid: str
    server_number: int


class CreateReport(ReportBase):
    pass


class UpdateReport(ReportBase):
    pass


class Report(ReportBase):
    id: int

    class Config:
        orm_mode = True
