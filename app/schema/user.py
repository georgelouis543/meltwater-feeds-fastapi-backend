import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserRole(str, Enum):
    admin = "admin"
    user = "user"  # default


class UserBase(BaseModel):
    user_email: str = Field(
        ...,
        min_length=13,
        description="firstname.lastname@meltwater.com"
    )
    user_name: str = Field(
        ...,
        min_length=1,
        description="firstname.lastname"
    )
    user_role: UserRole = Field(default=UserRole.user)

    @field_validator("user_email")
    def email_must_be_meltwater(cls, v: str):
        if not v.endswith("@meltwater.com"):
            raise ValueError("Email must be a meltwater.com address")
        return v


class UserCreate(UserBase):
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Date Created"
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Date Updated"
    )


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Date Updated"
    )


class UpdatedUserResponse(BaseModel):
    id: int
    user_email: str
    user_name: str
    role: UserRole

    class Config:
        from_attributes = True


