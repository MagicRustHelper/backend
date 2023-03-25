from app.db.crud import CRUDBase
from app.db.models import ModeratorSettings
from app.db.schemas import CreateModeratorSettings, UpdateModeratorSettings


class CRUDModeratorSettings(CRUDBase[ModeratorSettings, CreateModeratorSettings, UpdateModeratorSettings]):
    pass


moderator_settings = CRUDModeratorSettings(ModeratorSettings)
