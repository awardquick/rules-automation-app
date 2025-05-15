from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

# Shared base schema for all application-related schemas


class ApplicationBase(BaseModel):
    family_status: Optional[Literal["new", "returning"]] = None
    business_owner: bool
    filed_us_taxes: bool
    tax_year: int

    model_config = ConfigDict(from_attributes=True)


class ApplicationCreate(ApplicationBase):
    applicant_name: str
    applicant_email: EmailStr
    submitted_at: Optional[datetime] = None


class ApplicationResponse(ApplicationBase):
    id: int
    applicant_name: str
    applicant_email: EmailStr
    submitted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
