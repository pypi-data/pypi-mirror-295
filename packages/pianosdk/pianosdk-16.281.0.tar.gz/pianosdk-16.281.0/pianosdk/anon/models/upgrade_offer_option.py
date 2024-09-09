from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional


class UpgradeOfferOption(BaseModel):
    term_change_option_id: Optional[str] = None
    subscription_from_id: Optional[str] = None
    subscription_from_billing_plan: Optional[str] = None
    subscription_from_billing_period: Optional[str] = None
    term_from_id: Optional[str] = None
    term_from_name: Optional[str] = None
    term_from_type: Optional[str] = None
    access_period_from_id: Optional[str] = None
    access_period_from_name: Optional[str] = None
    resource_from_name: Optional[str] = None
    term_to_id: Optional[str] = None
    term_to_name: Optional[str] = None
    term_to_type: Optional[str] = None
    access_period_to_id: Optional[str] = None
    access_period_to_name: Optional[str] = None
    resource_to_name: Optional[str] = None
    resource_to_id: Optional[str] = None
    base_term_to_billing_plan: Optional[str] = None
    term_to_billing_period: Optional[str] = None
    billing_timing: Optional[int] = None
    immediate_access: Optional[bool] = None
    billing_date: Optional[datetime] = None
    billing_date_text: Optional[str] = None
    description: Optional[str] = None
    prorated_payment: Optional[str] = None


UpgradeOfferOption.model_rebuild()
