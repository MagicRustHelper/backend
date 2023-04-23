from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import BaseDeclarative, intpk


class Report(BaseDeclarative):
    __tablename__ = 'reports'

    id: Mapped[intpk]
    author_nickname: Mapped[str]
    report_steamid: Mapped[str]
    time: Mapped[datetime] = mapped_column(insert_default=func.now())
    server_number: Mapped[int]
