from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional
from pianosdk.anon.models.upgrade_offer_option import UpgradeOfferOption
from typing import List


class UpgradeOfferData(BaseModel):
    change_options: Optional['List[UpgradeOfferOption]'] = None


UpgradeOfferData.model_rebuild()
