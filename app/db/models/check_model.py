from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import BaseDeclarative, intpk


class Check(BaseDeclarative):
    __tablename__ = 'checks'

    id: Mapped[intpk]
    steamid: Mapped[str]
    moderator_id: Mapped[int] = mapped_column(ForeignKey('moderators.id'))
    start: Mapped[int] = mapped_column(insert_default=func.current_timestamp())
    end: Mapped[Optional[int]] = mapped_column(insert_default=func.current_timestamp())
    server_number: Mapped[int] = mapped_column(nullable=True)
    is_ban: Mapped[bool] = mapped_column(default=False)
