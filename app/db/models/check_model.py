from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import BaseDeclarative, intpk


class Check(BaseDeclarative):
    __tablename__ = 'checks'

    id: Mapped[intpk]
    steamid: Mapped[int] = mapped_column(BigInteger)
    moderator_id: Mapped[int] = mapped_column(ForeignKey('moderators.id'))
    start: Mapped[datetime] = mapped_column(insert_default=func.now())
    end: Mapped[Optional[datetime]] = mapped_column(insert_default=func.now())
    server_number: Mapped[int] = mapped_column(nullable=True)
    is_ban: Mapped[bool] = mapped_column(default=False)
