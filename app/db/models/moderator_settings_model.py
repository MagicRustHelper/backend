from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column

from app.db import BaseDeclarative
from app.db.models import default


class ModeratorSettings(BaseDeclarative):
    __tablename__ = 'moderator_settings'

    moderator_id: Mapped[int] = mapped_column(ForeignKey('moderators.id'), primary_key=True)
    player_is_new: Mapped[int] = mapped_column(default=60)
    exclude_servers: Mapped[list[str]] = mapped_column(MutableList.as_mutable(ARRAY(String)), default_factory=list)
    include_reasons: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(String)), default_factory=lambda: default.DEFAULT_INCLUDE_REASONS
    )
    exclude_reasons: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(String)), default_factory=lambda: default.DEFAULT_EXCLUDE_REASONS
    )
