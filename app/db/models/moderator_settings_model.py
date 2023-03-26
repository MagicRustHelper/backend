from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column

from app.db import BaseDeclarative

TWO_MONTH = 60 * 60 * 24 * 60


class ModeratorSettings(BaseDeclarative):
    __tablename__ = 'moderator_settings'

    moderator_id: Mapped[int] = mapped_column(ForeignKey('moderators.id'), primary_key=True)
    player_is_new: Mapped[int] = mapped_column(default=TWO_MONTH)
    exclude_servers = Column(MutableList.as_mutable(ARRAY(String)))
    include_reasons = Column(MutableList.as_mutable(ARRAY(String)))
    exclude_reasons = Column(MutableList.as_mutable(ARRAY(String)))
