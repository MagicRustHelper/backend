from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db import BaseDeclarative, intpk


class Moderator(BaseDeclarative):
    __tablename__ = 'moderators'

    id: Mapped[intpk]
    name: Mapped[str]
    steamid: Mapped[int] = mapped_column(BigInteger, unique=True)
    vk_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(default=None)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_bot: Mapped[bool] = mapped_column(default=False)
