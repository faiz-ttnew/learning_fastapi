from pydantic import (
    BaseModel, 
    Field,
    EmailStr,
    field_validator,
    model_validator
)
from datetime import date, datetime
from typing import Self
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.common.enums import TicketStatus, TicketPriority

class TicketCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=1, max_length=5000)
    priority: TicketPriority = TicketPriority.MEDIUM

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_text(cls, value):
        return value.strip() if isinstance(value, str) else value

class TicketUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    priority: TicketPriority | None = None
    status: TicketStatus | None = None

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @model_validator(mode="after")
    def check_field(self):
        if not self.model_fields_set:
            raise ValueError("At least one field is required")
        for name in self.model_fields_set:
            if getattr(self, name) is None:
                raise ValueError(f"{name} cannot be null")
        return self

class TicketAssign(BaseModel):
    model_config = ConfigDict(extra="forbid")
    assigned_to: int = Field(gt=0)

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    created_by: int
    assigned_to: int | None
    created_at: datetime
    updated_at: datetime

class TicketBulkAssign(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_ids: list[int] = Field(min_length=1, max_length=100)
    assigned_to: int = Field(gt=0)

    @field_validator("ticket_ids")
    @classmethod
    def clean_ids(cls, value):
        if any(ticket_id <= 0 for ticket_id in value):
            raise ValueError("ticket_ids must be positive integers")
        # Remove Duplicates
        return list(dict.fromkeys(value))

class AssignedUser(BaseModel):
    id: int 
    name:str
    email: str

class TicketDetailWithAssignedUser(TicketResponse):
    assigned_to: AssignedUser | None = None

class TicketFilter(BaseModel):
    title: str | None = None
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    assigned_to: int | None = None
    created_by_name: str | None = None
