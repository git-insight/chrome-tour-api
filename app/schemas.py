# schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    provider: Optional[str] = None  # Social login provider
    provider_user_id: Optional[str] = None  # For social login provider
    mfa_secret: Optional[str] = None  # For MFA setup

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_deleted: bool
    last_login_ip: Optional[str]
    roles: List[str] = []  # List of role names

    class Config:
        orm_mode = True

# User MFA-related schemas
class MfaCreate(BaseModel):
    secret: str
    app_name: str  # E.g., 'Google', 'Microsoft', 'AWS'

class MfaVerify(BaseModel):
    token: str
    mfa_app: Optional[str]  # Optional: Used to specify which MFA app

class MfaVerifyResponse(BaseModel):
    success: bool
    message: Optional[str] = None

# Password Reset Token Schema
class PasswordResetCreate(BaseModel):
    email: EmailStr

class PasswordResetResponse(BaseModel):
    message: str

# Role schema
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int
    is_deleted: bool  # Include the `is_deleted` flag in the response

    class Config:
        orm_mode = True

# User Session schema (for user login session management)
class UserSessionCreate(BaseModel):
    user_id: int
    device: Optional[str] = None
    user_agent: Optional[str] = None

class UserSessionResponse(BaseModel):
    id: int
    user_id: int
    device: Optional[str]
    user_agent: Optional[str]
    login_at: datetime
    expires_at: Optional[datetime]
    revoked_at: Optional[datetime]

    class Config:
        orm_mode = True
