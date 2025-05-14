from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Shared base schema for all application-related schemas
class ApplicationBase(BaseModel):
    family_status: str  # 'new' or 'returning'
    business_owner: bool
    filed_us_taxes: bool
    tax_year: int
    model_config = ConfigDict(from_attributes=True)

# Inherits fields from ApplicationBase


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationResponse(ApplicationBase):
    id: int
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)
