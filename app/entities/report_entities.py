from pydantic import BaseModel


class ReportCount(BaseModel):
    steamid: str
    count: int
