"""
GraphQL Input and Output Types for User operations.

This module defines Strawberry GraphQL schema types for registering users,
verifying their accounts, and returning sanitized user data to the client.
"""

import strawberry
from typing import Optional


@strawberry.input
class UserRegisterInput:
    """
    GraphQL input type used for user registration.

    Attributes:
        username (str): The desired unique username of the user.
        email (str): A valid and unique email address.
        phone_number (Optional[str]): Optional phone number, which may be used for MFA or login.
        password (str): Raw password input from the user, to be hashed before storing.
        registration_ip (Optional[str]): IP address of the device at registration time.
        user_agent (Optional[str]): Device or browser metadata collected at registration.
        registered_via (Optional[str]): Source of registration, e.g., 'web', 'mobile'.
        registration_referrer (Optional[str]): Referring page or campaign, if applicable.
    """
    username: str
    email: str
    phone_number: Optional[str] = None
    password: str
    registration_ip: Optional[str] = None
    user_agent: Optional[str] = None
    registered_via: Optional[str] = None
    registration_referrer: Optional[str] = None


@strawberry.input
class UserVerifyInput:
    """
    GraphQL input type used to verify a user's email or phone number after registration.

    Attributes:
        email (str): The email address to verify.
        verification_code (str): The verification code sent to the user's email.
    """
    email: str
    verification_code: str


@strawberry.type
class UserType:
    """
    GraphQL output type representing a registered or verified user.

    This type is returned to the client after registration or user lookups,
    and omits all sensitive fields such as password hashes or MFA secrets.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): User's chosen username.
        email (str): User's email address.
        is_active (bool): Flag indicating if the user account is active.
        email_verified (bool): Flag indicating if the email has been verified.
    """
    id: int
    username: str
    email: str
    is_active: bool
    email_verified: bool
