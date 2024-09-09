from typing import Optional
from enum import Enum

from pydantic import BaseModel


class ProfileStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    NOT_FETCHED = "not_fetched"


class LicenseVerifiedHttpResponse(BaseModel):
    license_token: str | None = None
    license_id: str | None = None
    token_id: str | None = None
    token_secret: str | None = None
    is_valid: bool

    @classmethod
    def error(cls):
        return cls(
            license_token="",
            license_id="",
            token_id="",
            token_secret="",
            is_valid=False,
        )


class DownloadProjectHttpResponse(BaseModel):
    url: Optional[str] | None = None
    project_id: Optional[str] | None = None
    version: Optional[str] | None = None
    is_valid: Optional[bool] | None = None
    profile_id: Optional[str] | None = None
    profile_status: Optional[ProfileStatus] | None = None

    @classmethod
    def error(cls):
        return cls(
            url="",
            project_id="",
            version="",
            is_valid=False,
            profile_id="",
            profile_status=ProfileStatus.NOT_FETCHED,
        )


class AuthResponse(BaseModel):
    is_valid: bool
    token: Optional[str] = None
    message: Optional[str] = None
